#!/usr/bin/env python3
"""
H.264 to MP4 Bulk Converter
Convert all .h264 recordings to MP4 format
Supports individual conversion, merging, and batch processing
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil

# ============= CONFIGURATION =============

# Directories (relative to script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "recordings")      # Where .h264 files are
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "converted")      # Where MP4 files go

# Conversion options
DELETE_ORIGINALS = False    # Delete .h264 files after successful conversion
ADD_TIMESTAMP = True        # Add timestamp to output filename

# =========================================

class VideoConverter:
    def __init__(self):
        self.input_dir = Path(INPUT_DIR)
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.total_files = 0
        self.converted_files = 0
        self.failed_files = 0
        self.skipped_files = 0
        
    def check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_h264_files(self):
        """Get all .h264 files in input directory"""
        files = sorted(self.input_dir.glob("*.h264"))
        return files
    
    def get_output_filename(self, input_file):
        """Generate output MP4 filename"""
        stem = input_file.stem
        
        if ADD_TIMESTAMP:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{stem}_{timestamp}.mp4"
        else:
            output_name = f"{stem}.mp4"
        
        return self.output_dir / output_name
    
    def convert_file(self, input_file, output_file):
        """Convert single .h264 file to MP4"""
        try:
            # Use ffmpeg to copy video stream into MP4 container (no re-encoding)
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-c', 'copy',           # Copy codec (no re-encoding)
                '-movflags', '+faststart',  # Optimize for web playback
                '-y',                   # Overwrite output file
                str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, str(e)
    
    def merge_files(self, input_files, output_file):
        """Merge multiple .h264 files into one MP4"""
        try:
            # Create temporary concat file
            concat_file = self.output_dir / "concat_list.txt"
            
            with open(concat_file, 'w') as f:
                for file in input_files:
                    # Use absolute paths and escape special characters
                    f.write(f"file '{file.absolute()}'\n")
            
            # Merge using concat demuxer
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                '-movflags', '+faststart',
                '-y',
                str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Clean up concat file
            concat_file.unlink()
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, str(e)
    
    def get_file_size(self, file_path):
        """Get file size in MB"""
        return file_path.stat().st_size / (1024 * 1024)
    
    def convert_all_individual(self):
        """Convert each .h264 file to individual MP4"""
        print(f"\n{'='*60}")
        print("🎬 INDIVIDUAL CONVERSION MODE")
        print(f"{'='*60}")
        print(f"Input:  {self.input_dir}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")
        
        files = self.get_h264_files()
        self.total_files = len(files)
        
        if self.total_files == 0:
            print("❌ No .h264 files found!")
            return
        
        print(f"Found {self.total_files} file(s) to convert\n")
        
        for i, input_file in enumerate(files, 1):
            output_file = self.get_output_filename(input_file)
            
            # Skip if output already exists
            if output_file.exists() and not ADD_TIMESTAMP:
                print(f"[{i}/{self.total_files}] ⏭️  Skipped: {input_file.name} (already exists)")
                self.skipped_files += 1
                continue
            
            print(f"[{i}/{self.total_files}] 🔄 Converting: {input_file.name}")
            
            input_size = self.get_file_size(input_file)
            
            success, error = self.convert_file(input_file, output_file)
            
            if success:
                output_size = self.get_file_size(output_file)
                print(f"            ✅ Success: {output_file.name}")
                print(f"            📊 Size: {input_size:.1f} MB → {output_size:.1f} MB")
                
                self.converted_files += 1
                
                # Delete original if configured
                if DELETE_ORIGINALS:
                    input_file.unlink()
                    print(f"            🗑️  Deleted: {input_file.name}")
            else:
                print(f"            ❌ Failed: {error}")
                self.failed_files += 1
            
            print()
        
        self.show_summary()
    
    def merge_all(self):
        """Merge all .h264 files into one MP4"""
        print(f"\n{'='*60}")
        print("🎬 MERGE ALL MODE")
        print(f"{'='*60}")
        print(f"Input:  {self.input_dir}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")
        
        files = self.get_h264_files()
        self.total_files = len(files)
        
        if self.total_files == 0:
            print("❌ No .h264 files found!")
            return
        
        if self.total_files == 1:
            print("⚠️  Only one file found. Use individual conversion instead.")
            return
        
        print(f"Found {self.total_files} file(s) to merge\n")
        
        # Show files to be merged
        print("Files to merge:")
        total_size = 0
        for i, f in enumerate(files, 1):
            size = self.get_file_size(f)
            total_size += size
            print(f"  {i}. {f.name} ({size:.1f} MB)")
        
        print(f"\nTotal size: {total_size:.1f} MB\n")
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"merged_{timestamp}.mp4"
        
        print(f"🔄 Merging into: {output_file.name}\n")
        
        success, error = self.merge_files(files, output_file)
        
        if success:
            output_size = self.get_file_size(output_file)
            print(f"✅ Merge successful!")
            print(f"📊 Output: {output_file.name} ({output_size:.1f} MB)")
            
            if DELETE_ORIGINALS:
                print(f"\n🗑️  Deleting {len(files)} original files...")
                for f in files:
                    f.unlink()
                print("✅ Original files deleted")
        else:
            print(f"❌ Merge failed: {error}")
    
    def merge_by_date(self):
        """Merge files grouped by date"""
        print(f"\n{'='*60}")
        print("🎬 MERGE BY DATE MODE")
        print(f"{'='*60}")
        print(f"Input:  {self.input_dir}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")
        
        files = self.get_h264_files()
        
        if len(files) == 0:
            print("❌ No .h264 files found!")
            return
        
        # Group files by date
        date_groups = {}
        for f in files:
            # Extract date from filename (rec_YYYYMMDD_HHMMSS.h264)
            try:
                date_str = f.stem.split('_')[1]  # Get YYYYMMDD part
                if date_str not in date_groups:
                    date_groups[date_str] = []
                date_groups[date_str].append(f)
            except:
                print(f"⚠️  Skipping invalid filename: {f.name}")
        
        print(f"Found {len(date_groups)} date(s) with recordings:\n")
        
        for date_str, group_files in sorted(date_groups.items()):
            print(f"📅 Date: {date_str} ({len(group_files)} file(s))")
            
            total_size = sum(self.get_file_size(f) for f in group_files)
            print(f"   Total size: {total_size:.1f} MB")
            
            # Output filename
            output_file = self.output_dir / f"merged_{date_str}.mp4"
            
            if output_file.exists():
                print(f"   ⏭️  Skipped: {output_file.name} already exists")
                self.skipped_files += len(group_files)
                print()
                continue
            
            print(f"   🔄 Merging into: {output_file.name}")
            
            success, error = self.merge_files(group_files, output_file)
            
            if success:
                output_size = self.get_file_size(output_file)
                print(f"   ✅ Success: {output_size:.1f} MB")
                self.converted_files += len(group_files)
                
                if DELETE_ORIGINALS:
                    for f in group_files:
                        f.unlink()
                    print(f"   🗑️  Deleted {len(group_files)} original file(s)")
            else:
                print(f"   ❌ Failed: {error}")
                self.failed_files += len(group_files)
            
            print()
        
        self.show_summary()
    
    def show_summary(self):
        """Show conversion summary"""
        print(f"{'='*60}")
        print("📊 CONVERSION SUMMARY")
        print(f"{'='*60}")
        print(f"Total files:     {self.total_files}")
        print(f"Converted:       {self.converted_files} ✅")
        print(f"Skipped:         {self.skipped_files} ⏭️")
        print(f"Failed:          {self.failed_files} ❌")
        print(f"{'='*60}\n")

def show_menu():
    """Show interactive menu"""
    print(f"\n{'='*60}")
    print("🎬 H.264 to MP4 Bulk Converter")
    print(f"{'='*60}")
    print("\nConversion Modes:")
    print("  1. Convert all files individually (one MP4 per .h264)")
    print("  2. Merge all files into ONE MP4")
    print("  3. Merge files by date (one MP4 per day)")
    print("  4. Exit")
    print(f"\n{'='*60}")

def main():
    print("=" * 60)
    print("H.264 to MP4 Bulk Converter")
    print("=" * 60)
    
    # Create converter
    converter = VideoConverter()
    
    # Check ffmpeg
    print("\n🔍 Checking dependencies...")
    if not converter.check_ffmpeg():
        print("❌ ffmpeg is not installed!")
        print("\nPlease install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS:         brew install ffmpeg")
        print("  Windows:       Download from https://ffmpeg.org")
        return 1
    print("✅ ffmpeg found")
    
    # Check input directory
    if not converter.input_dir.exists():
        print(f"\n❌ Input directory not found: {INPUT_DIR}")
        print("Creating directory...")
        converter.input_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Directory created (but it's empty)")
        return 1
    
    # Check for files
    files = converter.get_h264_files()
    print(f"📁 Found {len(files)} .h264 file(s) in: {INPUT_DIR}")
    
    if len(files) == 0:
        print("\n⚠️  No .h264 files to convert!")
        return 0
    
    # Show menu
    while True:
        show_menu()
        
        choice = input("Select mode (1-4): ").strip()
        
        if choice == '1':
            converter.convert_all_individual()
            break
        elif choice == '2':
            converter.merge_all()
            break
        elif choice == '3':
            converter.merge_by_date()
            break
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please select 1-4.")
    
    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Conversion cancelled by user")
        exit(0)