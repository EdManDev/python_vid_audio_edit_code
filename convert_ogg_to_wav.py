#!/usr/bin/env python3
"""
Batch convert all .ogg audio files to .wav using ffmpeg.

Usage examples:
  - Convert in current directory:
      python convert_ogg_to_wav.py

  - Specify input and output directories:
      python convert_ogg_to_wav.py --input "path/to/ogg" --output "path/to/wav"

  - Overwrite existing .wav files:
      python convert_ogg_to_wav.py --overwrite

Requirements:
  - ffmpeg must be installed and available on PATH
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from shutil import which


def ensure_ffmpeg_available() -> None:
    """Exit with an error message if ffmpeg is not found on PATH."""
    if which("ffmpeg") is None:
        sys.stderr.write(
            "Error: ffmpeg not found.\n"
            "Install ffmpeg and ensure it is on your PATH, then retry.\n"
            "Windows: install from https://ffmpeg.org/ or via winget/choco.\n"
            "Linux: install via your package manager (e.g., apt install ffmpeg).\n"
        )
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert all .ogg files in a directory to .wav using ffmpeg."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path.cwd(),
        help="Directory containing .ogg files (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Directory to write .wav files (default: same as input)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing .wav files if present",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.ogg",
        help="Glob pattern for input files (default: *.ogg)",
    )
    return parser.parse_args()


def convert_file(input_file: Path, output_file: Path, overwrite: bool) -> bool:
    """Convert a single OGG file to WAV using ffmpeg. Returns True on success."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_cmd = [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-i",
        str(input_file),
        str(output_file),
    ]

    try:
        completed = subprocess.run(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
    except FileNotFoundError:
        # Extra safety in case ffmpeg disappears mid-run
        sys.stderr.write("ffmpeg not found while running conversion.\n")
        return False

    if completed.returncode == 0:
        return True

    # If file exists and overwrite disabled, ffmpeg returns non-zero; treat as skipped
    if not overwrite and output_file.exists():
        return True

    sys.stderr.write(
        f"Failed to convert {input_file.name}:\n{completed.stderr}\n"
    )
    return False


def main() -> None:
    ensure_ffmpeg_available()
    args = parse_args()

    input_dir: Path = args.input.resolve()
    output_dir: Path = args.output.resolve() if args.output else input_dir

    if not input_dir.exists() or not input_dir.is_dir():
        sys.stderr.write(f"Input directory does not exist or is not a directory: {input_dir}\n")
        sys.exit(1)

    ogg_files = sorted(input_dir.glob(args.pattern))
    ogg_files = [p for p in ogg_files if p.is_file()]

    if not ogg_files:
        print(f"No files matched pattern '{args.pattern}' in {input_dir}")
        return

    total = len(ogg_files)
    successes = 0
    for idx, ogg_path in enumerate(ogg_files, start=1):
        wav_path = output_dir / f"{ogg_path.stem}.wav"
        print(f"[{idx}/{total}] Converting: {ogg_path.name} -> {wav_path.name}")
        ok = convert_file(ogg_path, wav_path, overwrite=args.overwrite)
        if ok:
            successes += 1

    print(f"Done. {successes}/{total} files converted.")


if __name__ == "__main__":
    main()


