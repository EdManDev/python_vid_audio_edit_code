#!/usr/bin/env python3
"""
Audio File Splitter - Splits large audio files into ~25MB chunks at silent points
Usage: python3 audio_splitter.py <input_file> [output_directory]
"""

import os
import sys
import argparse
from pydub import AudioSegment
from pydub.silence import detect_silence

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def estimate_duration_for_target_size(audio, target_size_mb):
    """Estimate duration in milliseconds for target file size"""
    current_size_mb = len(audio.raw_data) / (1024 * 1024)
    ratio = target_size_mb / current_size_mb
    return int(len(audio) * ratio)

def find_best_split_point(audio, start_ms, target_end_ms, silence_thresh=-50, min_silence_len=500):
    """
    Find the best silent point to split the audio near the target end point
    """
    # Search window around target end point (±10% of chunk duration)
    search_window = min(30000, int((target_end_ms - start_ms) * 0.1))  # Max 30 seconds window
    search_start = max(start_ms, target_end_ms - search_window)
    search_end = min(len(audio), target_end_ms + search_window)
    
    # Extract the search segment
    search_segment = audio[search_start:search_end]
    
    # Detect silence in the search segment
    silent_ranges = detect_silence(
        search_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    
    if not silent_ranges:
        # If no silence found, try with more lenient parameters
        silent_ranges = detect_silence(
            search_segment,
            min_silence_len=200,  # Shorter silence
            silence_thresh=silence_thresh + 10  # Less strict threshold
        )
    
    if silent_ranges:
        # Find the silence range closest to our target
        target_offset = target_end_ms - search_start
        best_split = None
        min_distance = float('inf')
        
        for silence_start, silence_end in silent_ranges:
            # Use middle of silence range
            silence_middle = (silence_start + silence_end) // 2
            distance = abs(silence_middle - target_offset)
            
            if distance < min_distance:
                min_distance = distance
                best_split = search_start + silence_middle
        
        return best_split
    
    # If no silence found, return target end point
    return target_end_ms

def split_audio_file(input_file, output_dir, target_size_mb=25.0):
    """
    Split audio file into chunks of approximately target_size_mb
    """
    print(f"Loading audio file: {input_file}")
    
    # Load the audio file
    try:
        audio = AudioSegment.from_file(input_file)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return False
    
    # Get original file info
    original_size_mb = get_file_size_mb(input_file)
    print(f"Original file size: {original_size_mb:.2f} MB")
    print(f"Audio duration: {len(audio) / 1000:.2f} seconds")
    print(f"Audio format: {audio.frame_rate} Hz, {audio.channels} channels, {audio.sample_width * 8} bit")
    
    # Calculate number of chunks needed
    num_chunks = int(original_size_mb / target_size_mb) + (1 if original_size_mb % target_size_mb > 0 else 0)
    print(f"Estimated chunks needed: {num_chunks}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension for output naming
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    file_extension = os.path.splitext(input_file)[1]
    
    chunk_num = 1
    start_ms = 0
    
    while start_ms < len(audio):
        print(f"\nProcessing chunk {chunk_num}...")
        
        # Estimate target end point for this chunk
        remaining_audio = audio[start_ms:]
        target_duration = estimate_duration_for_target_size(remaining_audio, target_size_mb)
        target_end_ms = min(start_ms + target_duration, len(audio))
        
        # If this is the last chunk or we're close to the end, take everything remaining
        if target_end_ms >= len(audio) - 5000:  # Within 5 seconds of end
            end_ms = len(audio)
        else:
            # Find the best split point at a silent moment
            end_ms = find_best_split_point(audio, start_ms, target_end_ms)
        
        # Extract the chunk
        chunk = audio[start_ms:end_ms]
        
        # Generate output filename
        output_filename = f"part{chunk_num}{file_extension}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Export the chunk
        try:
            chunk.export(
                output_path,
                format=file_extension[1:] if file_extension else "wav",
                parameters=["-acodec", "copy"] if file_extension.lower() in ['.wav', '.flac'] else None
            )
            
            # Check output file size
            chunk_size_mb = get_file_size_mb(output_path)
            duration_sec = len(chunk) / 1000
            
            print(f"Saved: {output_filename}")
            print(f"  Size: {chunk_size_mb:.2f} MB")
            print(f"  Duration: {duration_sec:.2f} seconds")
            print(f"  Time range: {start_ms/1000:.2f}s - {end_ms/1000:.2f}s")
            
        except Exception as e:
            print(f"Error exporting chunk {chunk_num}: {e}")
            return False
        
        # Move to next chunk
        start_ms = end_ms
        chunk_num += 1
        
        # Safety check to avoid infinite loop
        if chunk_num > 1000:
            print("Error: Too many chunks generated. Stopping.")
            break
    
    print(f"\nSplitting complete! Created {chunk_num - 1} chunks in '{output_dir}'")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Split large audio files into ~25MB chunks at silent points",
        epilog="Example: python3 audio_splitter.py input.wav ./output_chunks"
    )
    parser.add_argument("input_file", help="Path to the input audio file")
    parser.add_argument("output_dir", nargs="?", default="./chunks", 
                       help="Output directory for chunks (default: ./chunks)")
    parser.add_argument("--size", type=float, default=25.0, 
                       help="Target chunk size in MB (default: 25.0)")
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        sys.exit(1)
    
    # Check if file is large enough to split
    file_size_mb = get_file_size_mb(args.input_file)
    if file_size_mb <= args.size:
        print(f"File size ({file_size_mb:.2f} MB) is smaller than target chunk size ({args.size} MB)")
        print("No splitting needed.")
        sys.exit(0)
    
    # Check if pydub is available
    try:
        import pydub
    except ImportError:
        print("Error: pydub library is required. Install it with:")
        print("pip install pydub")
        print("\nYou may also need ffmpeg:")
        print("- On Ubuntu/Debian: sudo apt install ffmpeg")
        print("- On macOS: brew install ffmpeg")
        print("- On Windows: Download from https://ffmpeg.org/")
        sys.exit(1)
    
    # Perform the split
    success = split_audio_file(args.input_file, args.output_dir, args.size)
    
    if success:
        print("✓ Audio splitting completed successfully!")
    else:
        print("✗ Audio splitting failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
