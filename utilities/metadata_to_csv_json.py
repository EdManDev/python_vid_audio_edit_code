#!/usr/bin/env python3
import csv
import json
import sys
import os


def parse_metadata(metadata_file):
    """Parse metadata file and return list of audio-transcription pairs."""
    if not os.path.exists(metadata_file):
        print(f"Error: Metadata file '{metadata_file}' not found.")
        return None

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        data = []
        for line in lines:
            line = line.strip()
            if line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 2:
                    audio_file = parts[0]
                    transcription = parts[1]
                    data.append({"audio": audio_file, "transcription": transcription})

        return data

    except Exception as e:
        print(f"Error processing metadata file: {e}")
        return None


def create_csv(data, output_csv):
    """Create CSV file from data."""
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["audio", "transcription"])

            for item in data:
                writer.writerow([item["audio"], item["transcription"]])

        print(f"CSV file '{output_csv}' created successfully.")
        return True
    except Exception as e:
        print(f"Error creating CSV file: {e}")
        return False


def create_json(data, output_json):
    """Create JSON file from data."""
    try:
        with open(output_json, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)

        print(f"JSON file '{output_json}' created successfully.")
        return True
    except Exception as e:
        print(f"Error creating JSON file: {e}")
        return False


def main():
    if len(sys.argv) == 1:
        metadata_file = "metadata.txt"
        output_base = "transcriptions"
    elif len(sys.argv) == 2:
        metadata_file = sys.argv[1]
        output_base = "transcriptions"
    elif len(sys.argv) == 3:
        metadata_file = sys.argv[1]
        output_base = sys.argv[2].replace(".csv", "").replace(".json", "")
    else:
        print("Usage: python metadata_to_csv.py [<metadata_file> [<output_base>]]")
        print("Example: python metadata_to_csv.py metadata.txt transcriptions")
        print(
            "Or run without arguments to use defaults: metadata.txt -> transcriptions.csv & transcriptions.json"
        )
        sys.exit(1)

    data = parse_metadata(metadata_file)
    if data is None:
        sys.exit(1)

    output_csv = f"{output_base}.csv"
    output_json = f"{output_base}.json"

    csv_success = create_csv(data, output_csv)
    json_success = create_json(data, output_json)

    if not (csv_success and json_success):
        sys.exit(1)


if __name__ == "__main__":
    main()
