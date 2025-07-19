import subprocess
import tempfile
import sys
import os
import logging

# ===========================
# ==== Configure logging ====
# ===========================
log_level = logging.ERROR
log_filename = 'audio_silence_cutter.log'
logger = logging.getLogger('')
logger.setLevel(log_level)
log_handler = logging.FileHandler(log_filename, delay=True)
logger.addHandler(log_handler)


def findSilences(filename, dB):
    """
    Returns a list:
      even elements (0,2,4, ...) denote silence start time
      odd elements (1,3,5, ...) denote silence end time
    """
    logging.debug(f"findSilences()")
    logging.debug(f"    - filename = {filename}")
    logging.debug(f"    - dB = {dB}")

    command = ["ffmpeg", "-i", filename,
               "-af", "silencedetect=n=" + str(dB) + "dB:d=0.5",
               "-f", "null", "-"]
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = str(output.stderr, 'utf-8')
    lines = s.split("\n")
    time_list = []
    logging.debug("  lines: ```\n" + "\n".join(lines) + "```\n\n")

    for line in lines:
        if "silencedetect" in line:
            words = line.split(" ")
            logging.debug("  words: " + str(words))
            for i in range(len(words)):
                if "silence_start" in words[i]:
                    try:
                        time_list.append(float(words[i+1]))
                    except (IndexError, ValueError):
                        continue
                if "silence_end" in words[i]:
                    try:
                        time_list.append(float(words[i+1]))
                    except (IndexError, ValueError):
                        continue

    print("Detected silence timestamps:", time_list)
    return time_list


def getAudioDuration(filename: str) -> float:
    logging.debug(f"getAudioDuration()")
    logging.debug(f"    - filename = {filename}")

    command = ["ffprobe", "-i", filename, "-v", "quiet",
               "-show_entries", "format=duration", "-hide_banner",
               "-of", "default=noprint_wrappers=1:nokey=1"]

    output = subprocess.run(command, stdout=subprocess.PIPE)
    s = str(output.stdout, "UTF-8")
    return float(s.strip())


def getSectionsOfNewAudio(silences, duration, BUFFER):
    """Returns timings for parts where the audio should be kept"""
    print("Silences before adding buffer:", str(silences))
    silences = add_buffer(silences, duration, BUFFER)
    print("Silences after adding buffer:", str(silences))
    sections = [0.0] + silences + [duration]
    print("Audio sections to keep:", str(sections))
    return sections


def add_buffer(silences, duration, BUFFER):
    """Adds a buffer of BUFFER seconds to the silences"""
    for i in range(len(silences)):
        if i == 0:
            silences[i] = max(0, silences[i] - BUFFER)
        elif i == len(silences) - 1:
            silences[i] = min(duration, silences[i] + BUFFER)
        elif i % 2 == 1:  # silence end
            silences[i] = max(silences[i] - BUFFER, silences[i-1], 0)
        elif i % 2 == 0:  # silence start
            silences[i] = min(duration, silences[i] + BUFFER, silences[i+1])
    return silences


def createAudioFilter(audioSectionTimings):
    """Creates FFmpeg audio filter for keeping non-silent sections"""
    segments = []
    for i in range(int(len(audioSectionTimings)/2)):
        start = audioSectionTimings[2*i]
        end = audioSectionTimings[2*i+1]
        if end > start:  # Only add valid segments
            segments.append(f"between(t,{start},{end})")
    
    if not segments:
        return "anull"  # Return null filter if no segments
    
    filter_expr = "+".join(segments)
    return f"aselect='{filter_expr}',asetpts=N/SR/TB"


def ffmpeg_run_audio(infile, audioFilter, outfile):
    logging.debug(f"ffmpeg_run_audio()")

    # Use temporary file for filter
    with tempfile.NamedTemporaryFile(mode="w", encoding="UTF-8", prefix="audio_filter", suffix=".txt", delete=False) as aFile:
        audioFilter_file = aFile.name
        aFile.write(audioFilter)

    try:
        command = ["ffmpeg", "-i", infile,
                   "-filter_script:a", audioFilter_file,
                   "-y", outfile]  # -y to overwrite output file
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
        return True
    finally:
        # Clean up temporary file
        try:
            os.unlink(audioFilter_file)
        except OSError:
            pass


def cut_audio_silences(infile, outfile, dB, BUFFER):
    logging.debug(f"cut_audio_silences()")
    logging.debug(f"    - infile = {infile}")
    logging.debug(f"    - outfile = {outfile}")
    logging.debug(f"    - dB = {dB}")

    print("Detecting silences in audio...")
    silences = findSilences(infile, dB)
    
    if not silences:
        print("No silences detected. Copying original file...")
        subprocess.run(["ffmpeg", "-i", infile, "-c", "copy", "-y", outfile])
        return

    duration = getAudioDuration(infile)
    audioSegments = getSectionsOfNewAudio(silences, duration, BUFFER)

    audioFilter = createAudioFilter(audioSegments)
    print("Audio filter:", audioFilter)

    print("Creating new audio file...")
    success = ffmpeg_run_audio(infile, audioFilter, outfile)
    
    if success:
        print(f"Successfully created: {outfile}")
    else:
        print("Error creating audio file")


def printHelp():
    print("Audio Silence Cutter")
    print("Usage:")
    print("   python audio_silence_cutter.py [input_file] [optional: output_file] [optional: dB_threshold]")
    print("")
    print("Arguments:")
    print("   input_file    : Input audio file (.mp3, .wav, etc.)")
    print("   output_file   : Output audio file (default: [input]_cut.[ext])")
    print("   dB_threshold  : Silence threshold in dB (default: -30)")
    print("")
    print("Examples:")
    print("   python audio_silence_cutter.py audio.mp3")
    print("   python audio_silence_cutter.py audio.wav output.wav")
    print("   python audio_silence_cutter.py podcast.mp3 clean_podcast.mp3 -35")
    print("")
    print("dB Threshold Guide:")
    print("   -20 to -25: Very aggressive (removes low background noise)")
    print("   -30 to -35: Moderate (good for most recordings)")
    print("   -40 to -50: Conservative (only removes obvious silence)")
    print("")
    print("Dependencies:")
    print("   - FFmpeg (with ffprobe)")


def main():
    logging.debug(f"main()")
    args = sys.argv[1:]
    print("Arguments:", str(args))
    
    if len(args) < 1 or args[0] == "--help":
        printHelp()
        return

    infile = args[0]

    if not os.path.isfile(infile):
        print(f"ERROR: Input file not found: {infile}")
        return

    # Check if file is audio format
    ext = os.path.splitext(infile)[1].lower()
    if ext not in ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']:
        print(f"Warning: {ext} may not be a supported audio format")

    # Set default values for optional arguments
    tmp = os.path.splitext(infile)
    outfile = tmp[0] + "_cut" + tmp[1]

    if len(args) >= 2:
        outfile = args[1]

    dB = -30  # Default threshold for audio
    BUFFER = 0.1  # Shorter buffer for audio

    if len(args) >= 3:
        try:
            dB = int(args[2])
        except ValueError:
            print(f"Invalid dB value: {args[2]}. Using default: {dB}")

    print(f"Input: {infile}")
    print(f"Output: {outfile}")
    print(f"Silence threshold: {dB}dB")
    print(f"Buffer: {BUFFER}s")

    cut_audio_silences(infile, outfile, dB, BUFFER)


if __name__ == "__main__":
    main()