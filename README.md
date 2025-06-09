# Video Silence Cutter

A Python script for removing silent sections from videos using FFmpeg.

## Features
- Detect silent sections by audio threshold
- Automatically cut silent portions
- Adjustable silence detection sensitivity (-50dB to -25dB)
- Buffer periods around cuts for natural transitions

## Requirements
- Python 3.8+
- FFmpeg (system installation with ffprobe)

## Installation
```bash
# Install FFmpeg on Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

## Usage
```bash
# Basic usage (outputs rename your input video.mp4 to lecture.mp4 and run cmd below)
python main.py lecture.mp4

# Custom output file
python main.py input.mp4 output.mp4

# Adjust silence detection sensitivity (default: -25dB)
python main.py input.mp4 output.mp4 -30

# Example: Process video with aggressive silence cutting
python main.py lecture.mp4 lecture_edited.mp4 -35
```

## Configuration
- Buffer time: 0.2 seconds (hardcoded) to prevent abrupt cuts
- Logs saved to silence_cutter.log

## Notes
- Preserves original video/audio quality
- Processing time depends on video length and system resources