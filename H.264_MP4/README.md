# H.264 to MP4 Bulk Converter

Convert your recorded `.h264` video files to `.mp4` format with multiple conversion modes.

## 📋 Overview

This script converts H.264 raw video files (from the network recorder) into MP4 container format for better compatibility with video players, editors, and sharing platforms.

**Key Features:**
- ✅ Three conversion modes (individual, merge all, merge by date)
- ✅ No re-encoding (fast, no quality loss)
- ✅ Automatic file organization
- ✅ Progress tracking and statistics
- ✅ Optional auto-delete of originals
- ✅ Skip already converted files

## 🚀 Quick Start

### Prerequisites

Install ffmpeg (if not already installed):

```bash
# Ubuntu/Debian/Raspberry Pi
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Basic Usage

1. **Place the script** next to your `recordings` folder:
   ```
   your-folder/
   ├── convert_h264_to_mp4.py
   └── recordings/
       ├── rec_20250106_140000.h264
       ├── rec_20250106_140500.h264
       └── rec_20250106_141000.h264
   ```

2. **Make it executable:**
   ```bash
   chmod +x convert_h264_to_mp4.py
   ```

3. **Run the script:**
   ```bash
   ./convert_h264_to_mp4.py
   ```

4. **Select conversion mode** from the interactive menu:
   ```
   1. Convert all files individually
   2. Merge all files into ONE MP4
   3. Merge files by date
   4. Exit
   ```

## 🎬 Conversion Modes

### Mode 1: Individual Conversion
**What it does:** Converts each `.h264` file to a separate `.mp4` file

**Use case:** 
- Keep recordings as separate segments
- Easy to find specific time periods
- Selective playback

**Example:**
```
Input:
  rec_20250106_140000.h264
  rec_20250106_140500.h264
  rec_20250106_141000.h264

Output:
  rec_20250106_140000.mp4
  rec_20250106_140500.mp4
  rec_20250106_141000.mp4
```

### Mode 2: Merge All Files
**What it does:** Combines ALL `.h264` files into ONE big MP4

**Use case:**
- Create continuous recording from all segments
- Watch entire recording session
- Archive complete footage

**Example:**
```
Input:
  rec_20250106_140000.h264
  rec_20250106_140500.h264
  rec_20250106_141000.h264

Output:
  merged_20250106_143022.mp4  (all combined)
```

### Mode 3: Merge by Date
**What it does:** Groups files by date and creates one MP4 per day

**Use case:**
- Organize recordings by day
- Review daily footage easily
- Balanced between individual and full merge

**Example:**
```
Input:
  rec_20250106_140000.h264
  rec_20250106_140500.h264
  rec_20250107_090000.h264
  rec_20250107_090500.h264

Output:
  merged_20250106.mp4  (Jan 6 recordings)
  merged_20250107.mp4  (Jan 7 recordings)
```

## ⚙️ Configuration

Edit the script to customize behavior:

```python
# Directories
INPUT_DIR = os.path.join(SCRIPT_DIR, "recordings")   # Input folder
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "converted")   # Output folder

# Options
DELETE_ORIGINALS = False    # Delete .h264 after conversion?
ADD_TIMESTAMP = True        # Add timestamp to individual files?
```

### DELETE_ORIGINALS

**`False` (default - recommended):**
- Keeps original `.h264` files after conversion
- Safer - you can reconvert if needed
- Uses more disk space

**`True` (use with caution):**
- Deletes `.h264` files after successful conversion
- Saves disk space
- ⚠️ Cannot undo - originals are permanently deleted

### ADD_TIMESTAMP

**`True` (default):**
- Adds conversion timestamp to filename
- Example: `rec_20250106_140000_20250106_143022.mp4`
- Prevents overwriting if you convert multiple times

**`False`:**
- Uses original filename
- Example: `rec_20250106_140000.mp4`
- Skips files that already exist

## 📁 File Structure

```
your-folder/
├── convert_h264_to_mp4.py       # Converter script
├── network_stream_recorder.py   # Recording script
├── recordings/                  # Input directory (auto-created by recorder)
│   ├── rec_20250106_140000.h264
│   ├── rec_20250106_140500.h264
│   ├── rec_20250106_141000.h264
│   └── ...
└── converted/                   # Output directory (auto-created by converter)
    ├── rec_20250106_140000.mp4
    ├── rec_20250106_140500.mp4
    ├── merged_20250106.mp4
    └── ...
```

## 🎯 Common Use Cases

### 1. Daily Review Workflow
```bash
# Record all day with network_stream_recorder.py
# At end of day, convert by date
./convert_h264_to_mp4.py
# Select mode: 3 (Merge by date)
# Result: One MP4 per day for easy review
```

### 2. Archive Entire Week
```bash
# Let recordings accumulate for a week
# Then merge all into one file
./convert_h264_to_mp4.py
# Select mode: 2 (Merge all)
# Result: One large MP4 with entire week
```

### 3. Keep Segments Separate
```bash
# Convert all segments individually
./convert_h264_to_mp4.py
# Select mode: 1 (Individual)
# Result: Easy to find specific time periods
```

## 💡 Tips & Best Practices

### Storage Management
1. **Monitor disk space** before converting (MP4s are similar size to H.264)
2. **Set DELETE_ORIGINALS=True** only if you're sure you don't need originals
3. **Test first** - convert a few files before batch processing
4. **Backup important footage** before deleting originals

### Conversion Speed
- **No re-encoding** = very fast conversion (just container change)
- 5-minute segment = ~2-5 seconds to convert
- Limited by disk I/O, not CPU
- Can process hundreds of files quickly

### Quality
- **Zero quality loss** - video stream is copied as-is
- No compression artifacts introduced
- Same bitrate as original recording
- Professional broadcast quality maintained

### File Naming
**Recording format:** `rec_YYYYMMDD_HHMMSS.h264`
- `rec` = recording prefix
- `YYYYMMDD` = date (20250106 = Jan 6, 2025)
- `HHMMSS` = time (140000 = 2:00:00 PM)

**Merged output:** `merged_YYYYMMDD_HHMMSS.mp4` or `merged_YYYYMMDD.mp4`

## 🔧 Troubleshooting

### "ffmpeg is not installed"
**Solution:**
```bash
# Install ffmpeg
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### "No .h264 files found"
**Cause:** Script can't find recordings folder or it's empty

**Solution:**
1. Check recordings folder exists: `ls recordings/`
2. Verify .h264 files are there: `ls recordings/*.h264`
3. Run from correct directory (same folder as recordings)

### "Permission denied"
**Solution:**
```bash
chmod +x convert_h264_to_mp4.py
```

### Conversion fails/hangs
**Possible causes:**
- Corrupted .h264 file (incomplete recording)
- Disk full (no space for output)
- File in use (recording still in progress)

**Solution:**
1. Check disk space: `df -h`
2. Verify .h264 file is complete (not 0 bytes)
3. Stop recorder before converting

### MP4 won't play
**Possible causes:**
- Original .h264 file was corrupted
- Conversion interrupted

**Solution:**
1. Re-convert the file
2. Try different player (VLC recommended)
3. Check original .h264 file plays correctly

### Slow conversion
**Normal:** Conversion should be very fast (2-5 sec per 5-min segment)

**If slow:**
- Check disk health (may be failing)
- Close other disk-intensive programs
- Use SSD instead of HDD if possible

## 📊 Performance Examples

**Individual conversion (Mode 1):**
- 100 segments (5 min each) = ~8 hours of video
- Conversion time: ~3-5 minutes
- Output: 100 separate MP4 files

**Merge all (Mode 2):**
- 288 segments (5 min each) = 24 hours of video
- Conversion time: ~5-10 minutes
- Output: 1 large MP4 file

**Merge by date (Mode 3):**
- 7 days of recordings (24 hours/day)
- Conversion time: ~10-15 minutes
- Output: 7 MP4 files (one per day)

## 🎥 Playing Converted Videos

### Recommended Players

**VLC Media Player** (Best compatibility)
```bash
vlc converted/rec_20250106_140000.mp4
```

**ffplay** (Lightweight)
```bash
ffplay converted/rec_20250106_140000.mp4
```

**mpv** (Advanced)
```bash
mpv converted/rec_20250106_140000.mp4
```

### Video Editing

MP4 files can be imported into:
- **DaVinci Resolve** (free, professional)
- **Adobe Premiere Pro**
- **Final Cut Pro**
- **iMovie**
- **OpenShot** (free, simple)
- **Kdenlive** (free, Linux)

### Sharing

Upload to:
- YouTube
- Google Drive
- Dropbox
- Vimeo
- Social media platforms

## 🔄 Workflow Integration

### Automated Daily Conversion

Create a cron job to auto-convert each night:

```bash
# Edit crontab
crontab -e

# Add line to convert daily at 2 AM (Mode 3 - by date)
0 2 * * * cd /path/to/folder && echo "3" | ./convert_h264_to_mp4.py
```

### Integration with Recording

**Option 1: Manual (recommended)**
1. Let recordings accumulate
2. Periodically run converter
3. Review and archive

**Option 2: Automated**
1. Run converter as scheduled task
2. Set DELETE_ORIGINALS=True to save space
3. Archive converted files elsewhere

## 📝 Advanced Usage

### Convert Specific Files Only

Temporarily move unwanted files:
```bash
mkdir temp
mv recordings/rec_20250105*.h264 temp/
./convert_h264_to_mp4.py
mv temp/*.h264 recordings/
```

### Custom Output Directory

Edit script:
```python
OUTPUT_DIR = "/path/to/custom/output"
```

### Preserve Originals in Archive

```bash
# Copy originals to archive before converting
cp -r recordings/ archive_$(date +%Y%m%d)/

# Then convert with DELETE_ORIGINALS=True
./convert_h264_to_mp4.py
```

## 🆘 Getting Help

If you encounter issues:

1. **Check ffmpeg:** `ffmpeg -version`
2. **Verify files exist:** `ls -lh recordings/`
3. **Check disk space:** `df -h`
4. **Test single file manually:**
   ```bash
   ffmpeg -i recordings/rec_20250106_140000.h264 -c copy test.mp4
   ```
5. **Check file permissions:** `ls -l convert_h264_to_mp4.py`

## 🔐 Notes

- **No internet required** - all processing is local
- **No quality loss** - just container change (H.264 → MP4)
- **Fast processing** - no re-encoding needed
- **Safe operation** - originals preserved by default
- **Portable format** - MP4 works everywhere

## 📈 Storage Calculations

**H.264 vs MP4 file sizes:**
- Nearly identical (MP4 adds ~0.1% overhead for container)
- Both use H.264 codec internally
- MP4 just adds metadata wrapper

**Example:**
- Original: `rec_20250106_140000.h264` (75.2 MB)
- Converted: `rec_20250106_140000.mp4` (75.3 MB)
- Difference: Negligible

**When to delete originals:**
- If disk space is limited
- After verifying conversions play correctly
- When you're sure you won't need to reconvert

## 📜 License

Use freely for personal or commercial projects.

---

**Quick Reference:**
- Script: `convert_h264_to_mp4.py`
- Input: `./recordings/*.h264`
- Output: `./converted/*.mp4`
- Requirements: ffmpeg
- Speed: ~2-5 seconds per 5-minute segment
- Quality: Zero loss (copy mode)