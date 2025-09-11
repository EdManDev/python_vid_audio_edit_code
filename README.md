# Video and Audio Processing Tools

A comprehensive collection of Python scripts for video/audio processing including silence removal, format conversion, and file management using FFmpeg.

## Scripts Included

### Core Processing Scripts

#### 1. Audio Silence Cutter (`audio_silence_cutter.py`)
Removes silent sections from audio files (.mp3, .wav, .flac, .m4a, .aac, .ogg) with configurable thresholds and buffer periods.

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

#### 6. Audio File Splitter (`split_it.py`)
Intelligently splits large audio files into smaller chunks of approximately 25 MB each, while preserving audio quality and splitting only at silent points to avoid cutting words or introducing audio artifacts.

#### 7. File Renamer (`file_renamer_script.py`)
Batch renames files by removing "- Made with Clipchamp" text from filenames. Supports dry-run mode and confirmation prompts.

### Utility Scripts (`utilities/`)

#### 8. Metadata Converter (`metadata_to_csv_json.py`)
Converts metadata files (pipe-separated format) to both CSV and JSON formats for data processing workflows.

#### 9. Audio Format Converter (`convert_audio_to_22k_mono.py`)
Converts WAV files to 22kHz mono format using librosa. Supports batch processing and recursive folder scanning.

#### 10. LJSpeech Dataset Generator (`simple script.py`)
Generates folder structure for LJSpeech-1.1 processing from mimic-recording-studio database (legacy script).

## Features
- **Silence Detection & Removal**: Detect silent sections by audio threshold and automatically cut them
- **Adjustable Sensitivity**: Configurable silence detection thresholds (-20dB to -50dB)
- **Buffer Management**: Smart buffer periods around cuts for natural transitions
- **Audio File Splitting**: Intelligently split large audio files into smaller chunks at silent points
- **Size-based Splitting**: Create chunks based on file size (bytes), not duration
- **Quality Preservation**: Maintains original audio format and quality during splitting
- **Format Conversion**: Convert between various audio/video formats (MP4→MP3, M4A→WAV, OGG→WAV)
- **Batch Processing**: Process multiple files with glob patterns and directory support
- **File Management**: Batch rename files with pattern matching and dry-run capabilities
- **Metadata Processing**: Convert metadata files to CSV/JSON for data workflows
- **Audio Optimization**: Convert audio to specific formats (22kHz mono) for ML/AI applications

## Requirements

### Core Requirements
- **Python 3.8+**
- **FFmpeg** (system installation with ffprobe)
  - Windows: `winget install Gyan.FFmpeg` or `choco install ffmpeg`
  - Linux (Debian/Ubuntu): `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

### Optional Dependencies
For specific scripts:
- **pydub**: Required for `split_it.py` (audio file splitting)
  ```bash
  pip install pydub
  ```
- **librosa** and **soundfile**: Required for `utilities/convert_audio_to_22k_mono.py`
  ```bash
  pip install librosa soundfile
  ```

## Installation
```bash
# Verify FFmpeg is available
ffmpeg -version

# (Optional) Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate  # Windows (PowerShell): .venv\\Scripts\\Activate.ps1

# Install dependencies for audio splitting
pip install pydub

# (Optional) Install utility dependencies
pip install librosa soundfile
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

### Video Processing (`video_silence_cutter.py`)
```bash
# Basic usage
python3 video_silence_cutter.py input.mp4

# Custom output file
python3 video_silence_cutter.py input.mp4 edited.mp4

# Show help
python3 video_silence_cutter.py --help
```

### Audio File Splitting (`split_it.py`)
```bash
# Basic usage - Split audio file into ~25MB chunks in ./chunks directory
python3 split_it.py your_audio_file.mp3

# Custom output directory
python3 split_it.py your_audio_file.mp3 ./my_output_folder

# Custom chunk size (30MB instead of 25MB)
python3 split_it.py your_audio_file.wav ./output --size 30.0

# Show help
python3 split_it.py --help
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

## Silence Threshold Guide
- **-20 to -25dB**: Very aggressive (removes low background noise)
- **-30 to -35dB**: Moderate (good for most recordings)
- **-40 to -50dB**: Conservative (only removes obvious silence)

## Configuration

### Audio Processing (`audio_silence_cutter.py`)
- Buffer time: 0.1 seconds
- Logs saved to: `audio_silence_cutter.log`
- Default threshold: -30dB
- Silence detection: 0.5 seconds minimum

### Video Processing (`video_silence_cutter.py`)
- Buffer time: 0.2 seconds
- Logs saved to: `silence_cutter.log`
- Default threshold: -25dB
- Silence detection: 1.0 seconds minimum

## Supported Formats

### Video Input (for silence cutting and conversion)
- .mp4, .avi, .mov, .mkv, .webm (any FFmpeg-supported video format)

### Audio Input/Output
- **Input**: .mp3, .wav, .flac, .m4a, .aac, .ogg (any FFmpeg-supported audio format)
- **Output**: Same as input formats, plus conversion targets

### Format Conversions
- **MP4 → MP3**: 192kbps, 44.1kHz stereo
- **M4A → WAV**: Uncompressed WAV format
- **OGG → WAV**: Uncompressed WAV format
- **WAV → 22kHz Mono**: For ML/AI applications

## Audio File Splitting Details

### Features
- 🎯 **Size-based splitting**: Creates chunks based on file size (bytes), not duration
- 🔇 **Silent point detection**: Splits only at quiet moments to avoid cutting words
- 🎵 **Quality preservation**: Maintains original audio format and quality
- 📁 **Flexible output**: Custom output directories and chunk sizes
- 🔄 **Multiple formats**: Supports MP3, WAV, FLAC, M4A, and more
- 📊 **Progress tracking**: Detailed information about each chunk created

### How It Works
1. **Analyzes** the input file size and estimates number of chunks needed
2. **Calculates** target duration for each chunk based on size ratio
3. **Searches** for silent points within ±10% of the target split location
4. **Falls back** to more lenient silence detection if no quiet moments found
5. **Exports** chunks maintaining original quality and format
6. **Provides** detailed progress information for each chunk

### Example Output
```
Loading audio file: videoplayback.mp3
Original file size: 156.43 MB
Audio duration: 3847.50 seconds
Audio format: 44100 Hz, 2 channels, 16 bit
Estimated chunks needed: 7

Processing chunk 1...
Saved: part1.mp3
  Size: 24.98 MB
  Duration: 612.34 seconds
  Time range: 0.00s - 612.34s

Processing chunk 2...
Saved: part2.mp3
  Size: 24.95 MB
  Duration: 608.12 seconds
  Time range: 612.34s - 1220.46s

...

✓ Audio splitting completed successfully!
```

### Advanced Options
| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Path to audio file to split | Required |
| `output_dir` | Directory for output chunks | `./chunks` |
| `--size` | Target chunk size in MB | `25.0` |

### Tips for Best Results
- **Podcasts/Speech**: Works excellently due to natural pauses
- **Music**: May split between songs or during instrumental breaks
- **Dense audio**: Script will find the best available quiet moments
- **Large files**: Progress is shown for each chunk created

## Project Structure
```
python_vid_audio_edit_code/
├── audio_silence_cutter.py          # Audio silence removal
├── video_silence_cutter.py          # Video silence removal
├── convert_mp4_to_mp3.py            # MP4 to MP3 conversion
├── convert_m4a_to_wav.py            # M4A to WAV batch conversion
├── convert_ogg_to_wav.py            # OGG to WAV batch conversion
├── split_it.py                      # Audio file splitting
├── file_renamer_script.py           # Batch file renaming
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── utilities/
    ├── metadata_to_csv_json.py      # Metadata conversion
    ├── convert_audio_to_22k_mono.py # Audio format conversion
    └── simple script.py             # LJSpeech dataset generator
```

## Notes
- **Quality Preservation**: All scripts preserve original quality during processing
- **Performance**: Processing time depends on file size and system resources
- **Independence**: All scripts can run independently without dependencies on each other
- **Cleanup**: Temporary filter files are automatically cleaned up
- **Error Handling**: Comprehensive error handling and logging throughout
- **Cross-Platform**: Works on Windows, Linux, and macOS (requires FFmpeg)

### Additional Notes
- `utilities/convert_audio_to_22k_mono.py` requires `librosa` and `soundfile` packages
- `split_it.py` requires `pydub` package for audio file splitting
- On Windows, consider using WSL or ensure FFmpeg is on the PATH
- All batch conversion scripts support glob patterns for flexible file selection
- File renamer includes dry-run mode for safe testing

### Audio Splitter Troubleshooting
- **"ModuleNotFoundError: No module named 'pydub'"**: Install pydub using `pip install pydub`
- **"ffmpeg not found" or audio format errors**: Install ffmpeg system-wide
- **File too small message**: If your file is already smaller than 25MB, no splitting is needed
- **Permission errors**: Ensure you have write permissions to the output directory