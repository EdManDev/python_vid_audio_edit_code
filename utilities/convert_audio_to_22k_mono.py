#!/usr/bin/env python3
"""
Audio Converter Script
Converts WAV files to 22kHz mono format.
"""

import os
import argparse
from pathlib import Path
import librosa
import soundfile as sf


def convert_audio_file(input_path, output_path=None, overwrite=False):
    """
    Convert a WAV file to 22kHz mono format.

    Args:
        input_path (str): Path to the input WAV file
        output_path (str): Path for the output file (optional)
        overwrite (bool): Whether to overwrite the original file

    Returns:
        str: Path to the converted file
    """
    try:
        # Load audio file
        audio, sample_rate = librosa.load(input_path, sr=None, mono=False)

        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio)

        # Resample to 22kHz
        if sample_rate != 22050:
            audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=22050)

        # Determine output path
        if overwrite:
            output_file = input_path
        elif output_path:
            output_file = output_path
        else:
            # Create _converted suffix
            input_path_obj = Path(input_path)
            output_file = str(
                input_path_obj.parent
                / f"{input_path_obj.stem}_converted{input_path_obj.suffix}"
            )

        # Save the converted audio
        sf.write(output_file, audio, 22050)

        print(f"Converted: {input_path} -> {output_file}")
        return output_file

    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        return None


def scan_and_convert_folder(folder_path, overwrite=False, recursive=False):
    """
    Scan a folder for WAV files and convert them to 22kHz mono.

    Args:
        folder_path (str): Path to the folder to scan
        overwrite (bool): Whether to overwrite original files
        recursive (bool): Whether to scan subdirectories recursively
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Find WAV files
    if recursive:
        wav_files = list(folder.rglob("*.wav")) + list(folder.rglob("*.WAV"))
    else:
        wav_files = list(folder.glob("*.wav")) + list(folder.glob("*.WAV"))

    if not wav_files:
        print(f"No WAV files found in '{folder_path}'")
        return

    print(f"Found {len(wav_files)} WAV file(s) to convert...")

    converted_count = 0
    for wav_file in wav_files:
        result = convert_audio_file(str(wav_file), overwrite=overwrite)
        if result:
            converted_count += 1

    print(
        f"\nConversion complete! {converted_count}/{len(wav_files)} files converted successfully."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Convert WAV files to 22kHz mono format"
    )
    parser.add_argument("folder", nargs='?', default='.', help="Folder path containing WAV files (default: current directory)")
    parser.add_argument(
        "--overwrite",
        "-o",
        action="store_true",
        help="Overwrite original files instead of creating _converted versions",
    )
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="Scan subdirectories recursively"
    )

    args = parser.parse_args()

    scan_and_convert_folder(
        args.folder, overwrite=args.overwrite, recursive=args.recursive
    )


if __name__ == "__main__":
    main()
