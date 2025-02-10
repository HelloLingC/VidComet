import subprocess
import log_utils
import os

AUDIO_DIR = os.path.join(os.getcwd(), 'audio')
RAW_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'raw.mp3')

# Convert video into audio for whisper
def convert_to_audio(vid_path: str):
    log_utils.info('正在为视频分离音频文件....')
    if(not os.path.exists(AUDIO_DIR)):
        os.makedirs(AUDIO_DIR)
    subprocess.run(['ffmpeg', '-y', '-i', vid_path, RAW_AUDIO_FILE_PATH], check=True, stderr=subprocess.PIPE)
    log_utils.info(f'Converted {vid_path} into {RAW_AUDIO_FILE_PATH}')

def silence_detect():
    pass

def get_audio_duration(audio_file: str) -> float:
    """Get the duration of an audio file using ffmpeg."""
    cmd = ['ffmpeg', '-i', audio_file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = process.communicate()
    output = stderr.decode('utf-8', errors='ignore')
    
    try:
        duration_str = [line for line in output.split('\n') if 'Duration' in line][0]
        duration_parts = duration_str.split('Duration: ')[1].split(',')[0].split(':')
        duration = float(duration_parts[0])*3600 + float(duration_parts[1])*60 + float(duration_parts[2])
    except Exception as e:
        print(f"[red]❌ Error: Failed to get audio duration: {e}[/red]")
        duration = 0
    return duration

# split audio into 30mins for whisper
def split_audio(audio_file: str, frag_len:int=30*60, win: int=60):
    log_utils.info('[bold blue]Starting audio proprocessing...')

    duration = get_audio_duration(audio_file)
    segments = []
