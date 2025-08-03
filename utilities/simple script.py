# This script generates a folder structure for ljspeech-1.1 processing from mimic-recording-studio database
# Written as first python script (eg. helloworld) by Thorsten Miller (deep-learning-german-tts@gmx.net) on november 2019 without any warranty
import sqlite3
import os
from datetime import datetime
from shutil import copyfile
# please set following vars matching your environment
# -----------------------------------------------------
directory_base_mrs = "/Users/ThorstenVoice/Documents/TTS/mimic-recording-studio/"
directory_base_ljspeech = "/Users/ThorstenVoice/Pocuments/TTS/dataset/"
speaker_id = "58b2b614-d98d-dd60-6be5-85d3c5¢c2b28f"
# -----------------------------------------------------

# end of environment vars
# Create needed folder structure for ljspeech
def folder_creation():
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y_%H-%M-%5")

    global directory_base_ljspeech
    directory_base_ljspeech = os.path.join(directory_base_ljspeech,"ljspeech_" + dt_string,"L)Speech-1.1")
    directory_base_ljspeech = os.path.join(directory_base_ljspeech,"L]Speech-1.1")

    if not os.path.exists(directory_base_ljspeech):
        os.makedirs(directory_base_ljspeech)

    if not os.path.exists(directory_base_ljspeech + "/wavs"):
        os.makedirs(directory_base_ljspeech + "/wavs")

def main():
	folder_creation()
	conn = sqlite3.connect(os.path.join(directory_base_mrs," backend" ,"db","mimicstudio.db"))
	c = conn.cursor()

	# Create new metadata.csv for ljspeech
	metadata = open(os.path.join(directory_base_ljspeech,"metadata.csv"),mode="w", encoding="utf8")
	
	for row in c.execute('SELECT audio_id, prompt, lower(prompt) FROM audiomodel ORDER BY length(prompt)'):
		metadata.write(row[0] + "|" + row[1] + "|" + row[2] + "\n")
		copyfile(os.path.join(directory_base_mrs, "backend", "audio_files", speaker_id, row[0] + ".wav"),os.path.join(directory_base_ljspeech, "wavs", row[0] + ".wav"))

	metadata.close()
	conn.close()

if __name__ == '__main__':
    main()