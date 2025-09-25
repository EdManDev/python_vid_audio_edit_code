# Video and Audio Processing Tools

A comprehensive collection of Python scripts for video/audio processing including silence removal, format conversion, and file management using FFmpeg.

## Scripts Included

### Core Processing Scripts

#### 1. Audio Silence Cutter (`audio_silence_cutter.py`)
Removes silent sections from audio files (.mp3, .wav, .flac, .m4a, .aac, .ogg) with configurable thresholds and buffer periods.

**Key Features:**
- Intelligent silence detection using FFmpeg's silencedetect filter
- Configurable silence threshold (dB) and minimum silence duration (0.5 seconds)
- Smart buffer management around silence cuts for natural transitions
- Automatic audio duration detection
- Advanced filter generation using aselect and asetpts for seamless audio reconstruction
- Comprehensive error handling and logging
- Support for all major audio formats

#### 2. Video Silence Cutter (`video_silence_cutter.py`)
Detects and removes silent sections from video files while preserving both video and audio tracks.

### Format Conversion Scripts

#### 3. MP4 to MP3 Converter (`convert_mp4_to_mp3.py`)
Converts MP4 video files to high-quality MP3 audio format (192kbps, 44.1kHz).

#### 4. M4A to WAV Batch Converter (`convert_m4a_to_wav.py`)
Batch converts `.m4a` files to `.wav` using FFmpeg. Supports input/output folders, glob patterns, and overwrite mode.

#### 5. OGG to WAV Batch Converter (`convert_ogg_to_wav.py`)
Batch converts `.ogg` files to `.wav` using FFmpeg. Supports input/output folders, glob patterns, and overwrite mode.

### File Management Scripts

#### 6. File Renamer (`file_renamer_script.py`)
Batch renames files by removing "- Made with Clipchamp" text from filenames. Supports dry-run mode and confirmation prompts.

### Utility Scripts (`utilities/`)

#### 7. Metadata Converter (`metadata_to_csv_json.py`)
Converts metadata files (pipe-separated format) to both CSV and JSON formats for data processing workflows.

#### 8. Audio Format Converter (`convert_audio_to_22k_mono.py`)
Converts WAV files to 22kHz mono format using librosa. Supports batch processing and recursive folder scanning.

#### 9. LJSpeech Dataset Generator (`simple script.py`)
Generates folder structure for LJSpeech-1.1 processing from mimic-recording-studio database (legacy script).

## Features
- **Advanced Silence Detection**: Uses FFmpeg's silencedetect filter with configurable thresholds and minimum duration
- **Smart Audio Reconstruction**: Employs aselect and asetpts filters for seamless audio segment joining
- **Adjustable Sensitivity**: Configurable silence detection thresholds (-20dB to -50dB)
- **Buffer Management**: Smart buffer periods (0.1s for audio) around cuts for natural transitions
- **Format Support**: Comprehensive support for audio formats (.mp3, .wav, .flac, .m4a, .aac, .ogg)
- **Format Conversion**: Convert between various audio/video formats (MP4→MP3, M4A→WAV, OGG→WAV)
- **Batch Processing**: Process multiple files with glob patterns and directory support
- **File Management**: Batch rename files with pattern matching and dry-run capabilities
- **Metadata Processing**: Convert metadata files to CSV/JSON for data workflows
- **Audio Optimization**: Convert audio to specific formats (22kHz mono) for ML/AI applications
- **Comprehensive Logging**: Detailed logging with configurable levels for debugging

## Requirements

### Core Requirements
- **Python 3.8+**
- **FFmpeg** (system installation with ffprobe)
  - Windows: `winget install Gyan.FFmpeg` or `choco install ffmpeg`
  - Linux (Debian/Ubuntu): `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

### Python Dependencies
- **librosa** and **soundfile**: Required for `utilities/convert_audio_to_22k_mono.py`. These are listed in `requirements.txt`.

## Installation
```bash
# 1. Clone the repository
# git clone https://github.com/your-username/python_vid_audio_edit_code.git
# cd python_vid_audio_edit_code

# Verify FFmpeg is available
ffmpeg -version
ffprobe -version

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

# Install Python dependencies for utility scripts
pip install -r requirements.txt
```

## Usage

### Audio Silence Cutter (`audio_silence_cutter.py`)

**Basic Usage:**
```bash
# Process with default settings (-30dB threshold, 0.1s buffer)
python3 audio_silence_cutter.py podcast.mp3
# Output: podcast_cut.mp3

# Specify custom output file
python3 audio_silence_cutter.py audio.wav clean_audio.wav

# Custom threshold for more/less aggressive cutting
python3 audio_silence_cutter.py recording.mp3 output.mp3 -35

# Get detailed help
python3 audio_silence_cutter.py --help
```

**Advanced Examples:**
```bash
# Very aggressive silence removal (good for noisy recordings)
python3 audio_silence_cutter.py noisy_podcast.mp3 clean_podcast.mp3 -25

# Conservative silence removal (preserve natural pauses)
python3 audio_silence_cutter.py interview.wav clean_interview.wav -40

# Process multiple files
for file in *.mp3; do
    python3 audio_silence_cutter.py "$file"
done
```

### Video Processing (`video_silence_cutter.py`)
```bash
# Basic usage
python3 video_silence_cutter.py input.mp4

# Custom output file
python3 video_silence_cutter.py input.mp4 edited.mp4

# Show help
python3 video_silence_cutter.py --help
```

### MP4 to MP3 Conversion (`convert_mp4_to_mp3.py`)
```bash
# Basic usage (outputs to output.mp3)
python3 convert_mp4_to_mp3.py input.mp4

# Example
python3 convert_mp4_to_mp3.py video.mp4
```

### M4A to WAV Batch Conversion (`convert_m4a_to_wav.py`)
```bash
# Convert all .m4a files in the current directory to .wav
python3 convert_m4a_to_wav.py

# Specify input and output directories
python3 convert_m4a_to_wav.py --input "path/to/m4a" --output "path/to/wav"

# Use a custom glob pattern and overwrite existing .wav files
python3 convert_m4a_to_wav.py --pattern "**/*.m4a" --overwrite
```

### OGG to WAV Batch Conversion (`convert_ogg_to_wav.py`)
```bash
# Convert all .ogg files in the current directory to .wav
python3 convert_ogg_to_wav.py

# Specify input and output directories
python3 convert_ogg_to_wav.py --input "path/to/ogg" --output "path/to/wav"

# Use a custom glob pattern and overwrite existing .wav files
python3 convert_ogg_to_wav.py --pattern "**/*.ogg" --overwrite
```

### File Renaming (`file_renamer_script.py`)
```bash
# Rename files in current directory (with confirmation)
python3 file_renamer_script.py

# Specify input directory and pattern
python3 file_renamer_script.py --input "path/to/files" --pattern "*.mp4"

# Dry run to see what would be renamed
python3 file_renamer_script.py --dry-run

# Force rename without confirmation
python3 file_renamer_script.py --force
```

### Utility Scripts

#### Metadata Conversion (`utilities/metadata_to_csv_json.py`)
```bash
# Convert metadata file to CSV and JSON (default: metadata.txt -> transcriptions.csv/json)
python3 utilities/metadata_to_csv_json.py

# Specify input and output files
python3 utilities/metadata_to_csv_json.py metadata.txt output_data

# Example with custom files
python3 utilities/metadata_to_csv_json.py my_metadata.txt my_transcriptions
```

#### Audio Format Conversion (`utilities/convert_audio_to_22k_mono.py`)
```bash
# Convert WAV files in current directory to 22kHz mono
python3 utilities/convert_audio_to_22k_mono.py

# Convert specific folder
python3 utilities/convert_audio_to_22k_mono.py /path/to/wav/files

# Overwrite original files instead of creating _converted versions
python3 utilities/convert_audio_to_22k_mono.py --overwrite

# Recursively scan subdirectories
python3 utilities/convert_audio_to_22k_mono.py --recursive
```

## Audio Silence Detection Guide

### dB Threshold Reference
- **-20 to -25dB**: Very aggressive (removes low background noise, room tone)
- **-30 to -35dB**: Moderate (recommended for most recordings, good balance)
- **-40 to -50dB**: Conservative (only removes obvious silence, preserves natural pauses)

### How Silence Detection Works
1. **Detection**: FFmpeg's silencedetect filter identifies silence segments longer than 0.5 seconds
2. **Buffer Application**: Adds 0.1-second buffer around silence boundaries for natural transitions  
3. **Segment Extraction**: Uses aselect filter to keep non-silent portions
4. **Reconstruction**: Employs asetpts to create continuous audio timeline

### Troubleshooting Silence Detection
- **Too much audio removed**: Increase threshold (e.g., -25 → -35)
- **Not enough silence removed**: Decrease threshold (e.g., -35 → -25)
- **Choppy audio**: Check for very short segments, consider different threshold
- **No silences detected**: File may have constant background noise, try lower threshold

## Configuration

### Audio Processing (`audio_silence_cutter.py`)
- **Buffer time**: 0.1 seconds (around silence cuts)
- **Minimum silence duration**: 0.5 seconds (for detection)
- **Log file**: `audio_silence_cutter.log`
- **Log level**: ERROR (change `log_level` variable for more detail)
- **Default threshold**: -30dB
- **Supported formats**: .mp3, .wav, .flac, .m4a, .aac, .ogg

### Video Processing (`video_silence_cutter.py`)
- **Buffer time**: 0.2 seconds
- **Log file**: `silence_cutter.log`
- **Default threshold**: -25dB
- **Minimum silence duration**: 1.0 seconds

## Supported Formats

### Audio Input/Output (audio_silence_cutter.py)
- **Input**: .mp3, .wav, .flac, .m4a, .aac, .ogg
- **Output**: Same format as input (preserves original quality)
- **Quality**: Lossless processing (no re-encoding unless necessary)

### Video Input (for silence cutting and conversion)
- .mp4, .avi, .mov, .mkv, .webm (any FFmpeg-supported video format)

### Format Conversions
- **MP4 → MP3**: 192kbps, 44.1kHz stereo
- **M4A → WAV**: Uncompressed WAV format
- **OGG → WAV**: Uncompressed WAV format
- **WAV → 22kHz Mono**: For ML/AI applications

## Project Structure
```
python_vid_audio_edit_code/
├── audio_silence_cutter.py          # Audio silence removal (main script)
├── video_silence_cutter.py          # Video silence removal
├── convert_mp4_to_mp3.py            # MP4 to MP3 conversion
├── convert_m4a_to_wav.py            # M4A to WAV batch conversion
├── convert_ogg_to_wav.py            # OGG to WAV batch conversion
├── file_renamer_script.py           # Batch file renaming
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── utilities/
    ├── metadata_to_csv_json.py      # Metadata conversion
    ├── convert_audio_to_22k_mono.py # Audio format conversion
    └── simple script.py             # LJSpeech dataset generator
```

## Technical Details

### Audio Processing Algorithm
1. **Silence Detection**: Uses FFmpeg's `silencedetect` filter with configurable threshold and minimum duration
2. **Timestamp Extraction**: Parses FFmpeg output to extract silence start/end timestamps
3. **Buffer Application**: Adds protective buffer around silence boundaries to prevent audio cuts
4. **Filter Generation**: Creates complex FFmpeg filter using `aselect` and `asetpts` for seamless reconstruction
5. **Audio Reconstruction**: Processes audio through filter script for optimal performance

### Error Handling
- **File Validation**: Checks input file existence and format compatibility
- **Process Monitoring**: Monitors FFmpeg execution with detailed error reporting  
- **Cleanup**: Automatically removes temporary filter files
- **Logging**: Comprehensive logging system for debugging and monitoring

## Notes
- **Quality Preservation**: Lossless processing - no unnecessary re-encoding
- **Performance**: Processing time depends on file size; detection is typically fast
- **Memory Efficient**: Uses temporary files and streaming processing for large files
- **Cross-Platform**: Works on Windows, Linux, and macOS (requires FFmpeg)
- **Independence**: All scripts run independently without cross-dependencies
- **Backup Recommendation**: Original files are preserved (output uses different filename)

### Audio Processing Best Practices
- **Test First**: Try different thresholds on a small sample before batch processing
- **Monitor Output**: Check that silence detection worked as expected
- **Backup Originals**: Keep original files safe before processing
- **Format Consistency**: Output maintains input format and quality
- **Log Analysis**: Check log files if processing doesn't work as expected

### Additional Notes
- `utilities/convert_audio_to_22k_mono.py` requires `librosa` and `soundfile` packages
- On Windows, ensure FFmpeg is properly installed and accessible in PATH
- All batch conversion scripts support glob patterns for flexible file selection
- File renamer includes dry-run mode for safe testing
- Silence detection works best with consistent audio levels throughout the file