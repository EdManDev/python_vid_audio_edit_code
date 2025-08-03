# Video and Audio Processing Tools

Python scripts for video/audio processing including silence removal and format conversion using FFmpeg.

## Scripts Included

### 1. Audio Silence Cutter (`audio_silence_cutter.py`)
Optimized for audio-only files (.mp3, .wav, .flac, .m4a, .aac, .ogg).

### 2. Video Silence Cutter (`video_silence_cutter.py`)
Core silence detection functionality using FFmpeg for finding silent sections in video files.

### 3. MP4 to MP3 Converter (`mp4_to_mp3_converter.py`)
Converts MP4 video files to MP3 audio format with high quality output.

### 4. Utility Scripts (`utilities/`)
- **Metadata to CSV/JSON Converter** (`metadata_to_csv_json.py`): Converts metadata files to CSV or JSON format
- **Audio Format Converter** (`convert_audio_to_22k_mono.py`): Converts WAV files to 22kHz mono format
- **Simple Script** (`simple script.py`): Additional utility script

## Features
- Detect silent sections by audio threshold
- Automatically cut silent portions
- Adjustable silence detection sensitivity
- Buffer periods around cuts for natural transitions
- Separate optimizations for video vs audio processing
- Convert MP4 video files to high-quality MP3 audio

## Requirements
- Python 3.8+
- FFmpeg (system installation with ffprobe)

## Installation
```bash
# Install FFmpeg on Ubuntu/Debian or WSL Windows 
sudo apt update && sudo apt install ffmpeg

# Install FFmpeg on macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

## Usage

### Audio Processing (`audio_silence_cutter.py`)
```bash
# Basic usage
python3 audio_silence_cutter.py podcast.mp3

# Custom output file and threshold
python3 audio_silence_cutter.py audio.wav clean_audio.wav -35

# Get help
python3 audio_silence_cutter.py --help
```

### MP4 to MP3 Conversion (`mp4_to_mp3_converter.py`)
```bash
# Basic usage (outputs to output.mp3)
python3 mp4_to_mp3_converter.py input.mp4

# Example
python3 mp4_to_mp3_converter.py video.mp4
```

### Utility Scripts

#### Metadata Conversion (`utilities/metadata_to_csv_json.py`)
```bash
# Convert metadata file to CSV or JSON
python3 utilities/metadata_to_csv_json.py metadata.txt
```

#### Audio Format Conversion (`utilities/convert_audio_to_22k_mono.py`)
```bash
# Convert WAV to 22kHz mono format
python3 utilities/convert_audio_to_22k_mono.py input.wav
```

## Silence Threshold Guide
- **-20 to -25dB**: Very aggressive (removes low background noise)
- **-30 to -35dB**: Moderate (good for most recordings)
- **-40 to -50dB**: Conservative (only removes obvious silence)

## Configuration

### Audio Processing  
- Buffer time: 0.1 seconds
- Logs saved to: `audio_silence_cutter.log`
- Default threshold: -30dB
- Silence detection: 0.5 seconds minimum

## Supported Formats

### Video Input (for silence cutting and conversion)
- .mp4, .avi, .mov, .mkv, .webm (any FFmpeg-supported video format)

### Audio
- .mp3, .wav, .flac, .m4a, .aac, .ogg (any FFmpeg-supported audio format)

### Conversion
- Input: MP4 video files
- Output: MP3 audio files (192kbps, 44.1kHz)

## Notes
- Preserves original quality
- Processing time depends on file size and system resources
- Both scripts can run independently
- Temporary filter files are automatically cleaned up