#!/usr/bin/env python3

import sys
import os
import subprocess


def convert_mp4_to_mp3(input_file, output_file="output.mp3"):
    try:
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False

        if not input_file.lower().endswith(".mp4"):
            print(f"Error: Input file must be an MP4 file.")
            return False

        print(f"Converting {input_file} to {output_file}...")

        # Use ffmpeg to extract audio from video
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-vn",  # No video
            "-acodec",
            "mp3",  # Audio codec
            "-ab",
            "192k",  # Audio bitrate
            "-ar",
            "44100",  # Audio sample rate
            "-y",  # Overwrite output file
            output_file,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Conversion completed: {output_file}")
            return True
        else:
            print(f"Error during conversion: {result.stderr}")
            return False

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 mp4_to_mp3_converter.py input.mp4")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_mp4_to_mp3(input_file)


if __name__ == "__main__":
    main()
