# Silence Cutter Tools

Python scripts for removing silent sections from videos and audio files using FFmpeg.

## Scripts Included

### 1. Video Silence Cutter (`main.py`)
Removes silent sections from video files while preserving video and audio quality.

### 2. Audio Silence Cutter (`audio_silence_cutter.py`)
Optimized for audio-only files (.mp3, .wav, .flac, .m4a, .aac, .ogg).

## Features
- Detect silent sections by audio threshold
- Automatically cut silent portions
- Adjustable silence detection sensitivity
- Buffer periods around cuts for natural transitions
- Separate optimizations for video vs audio processing

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

### Video Processing (`main.py`)
```bash
# Basic usage
python main.py lecture.mp4

# Custom output file
python main.py input.mp4 output.mp4

# Adjust silence detection sensitivity (default: -25dB)
python main.py input.mp4 output.mp4 -30

# Example: Process video with aggressive silence cutting
python main.py lecture.mp4 lecture_edited.mp4 -35
```

### Audio Processing (`audio_silence_cutter.py`)
```bash
# Basic usage
python3 audio_silence_cutter.py podcast.mp3

# Custom output file and threshold
python3 audio_silence_cutter.py audio.wav clean_audio.wav -35

# Get help
python3 audio_silence_cutter.py --help
```

## Silence Threshold Guide
- **-20 to -25dB**: Very aggressive (removes low background noise)
- **-30 to -35dB**: Moderate (good for most recordings)
- **-40 to -50dB**: Conservative (only removes obvious silence)

## Configuration

### Video Processing
- Buffer time: 0.2 seconds
- Logs saved to: `silence_cutter.log`
- Default threshold: -25dB

### Audio Processing  
- Buffer time: 0.1 seconds
- Logs saved to: `audio_silence_cutter.log`
- Default threshold: -30dB
- Silence detection: 0.5 seconds minimum

## Supported Formats

### Video
- .mp4, .avi, .mov, .mkv, .webm (any FFmpeg-supported video format)

### Audio
- .mp3, .wav, .flac, .m4a, .aac, .ogg (any FFmpeg-supported audio format)

## Notes
- Preserves original quality
- Processing time depends on file size and system resources
- Both scripts can run independently
- Temporary filter files are automatically cleaned up