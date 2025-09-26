import os
import sys
from pydub import AudioSegment
import core

def find_audio_files(folder_path):
    audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
    audio_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))
    
    return audio_files


def main():
    if(os.getcwd() +'/core' not in sys.path):
        sys.path.append(os.getcwd() +'/core')
    
    folder = input("Input folder path: ")
    audio_files = find_audio_files(folder)

    for file_path in audio_files:
        # stereo = "Stereo" if is_stereo_pydub(file_path) else ""
        print(f"\033[1;36m{os.path.basename(file_path)}\033[0m ")
    
    num = int(input("Work on which audios? (0 for all): "))
    
    if(num == 0):
        ...
    elif num in range(len(audio_files)):
        
            core.start_preprocess(audio_files[num])


if __name__ == "__main__":
    main()
