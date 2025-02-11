import subprocess
from config_utils import *
import log_utils
import os

# Convert video into audio for whisper
def convert_to_audio(vid_path: str):
    log_utils.info('正在为视频分离音频文件....')
    if(not os.path.exists(AUDIO_DIR)):
        os.makedirs(AUDIO_DIR)
    subprocess.run(['ffmpeg', '-y', '-i', vid_path, RAW_AUDIO_FILE_PATH], check=True, stderr=subprocess.PIPE)
    log_utils.debug(f'Converted video into {RAW_AUDIO_FILE_PATH}')
    log_utils.info('成功分离音频文件！')

def enhance_vocals(vocals_ratio=2.50):
    # if not load_key("demucs"):
    #     return RAW_AUDIO_FILE_PATH
    try:
        log_utils.info(f"[cyan]🎙️ Enhancing vocals with volume ratio: {vocals_ratio}[/cyan]")
        ffmpeg_cmd = (
            f'ffmpeg -y -i "{VOCAL_AUDIO_FILE_PATH}" '
            f'-filter:a "volume={vocals_ratio}" '
            f'"{ENHANCED_VOCAL_PATH}"'
        )
        subprocess.run(ffmpeg_cmd, shell=True, check=True, capture_output=True)
        log_utils.info(f'已成功人声增强！')
        return ENHANCED_VOCAL_PATH
    except subprocess.CalledProcessError as e:
        log_utils.info(f"Error enhancing vocals: {str(e)}")
        return VOCAL_AUDIO_FILE_PATH  # Fallback to original vocals if enhancement fails

def compress_audio(input: str, output: str= COMPRESSED_AUDIO_PATH):
    if not os.path.exists(output):
        log_utils.info(f"正在压缩音频文件...")
        # 16000 Hz, 1 channel, (Whisper default) , 96kbps to keep more details as well as smaller file size
        subprocess.run([
            'ffmpeg', '-y', '-i', input, '-vn', '-b:a', '96k',
            '-ar', '16000', '-ac', '1', '-metadata', 'encoding=UTF-8',
            '-f', 'mp3', output
        ], check=True, stderr=subprocess.PIPE)
        log_utils.info("压缩成功！")
    return output

def silence_detect(audio_file, start:float, end:float)->list[float]:
    cmd = ['ffmpeg', '-y', '-i', audio_file, 
           '-ss', str(start), '-to', str(end),
           '-af', 'silencedetect=n=-30dB:d=0.5', 
           '-f', 'null', '-']
    
    output = subprocess.run(cmd, capture_output=True, text=True, 
                          encoding='utf-8').stderr
    
    return [float(line.split('silence_end: ')[1].split(' ')[0])
            for line in output.split('\n')
            if 'silence_end' in line]

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
def split_audio(audio_file: str, frag_len:int=30*60, window: int=60) -> list[tuple[float, float]]:
    log_utils.info('[bold blue]Starting audio proprocessing...')

    duration = get_audio_duration(audio_file)
    segments = []
    pos = 0
    while pos < duration:
        if duration - pos < frag_len:
            segments.append((pos, duration))
            break
        win_start = pos + frag_len - window
        win_end = min(win_start + 2 * window, duration)
        silences = silence_detect(audio_file, win_start, win_end)
    
        if silences:
            target_pos = frag_len - (win_start - pos)
            split_at = next((t for t in silences if t - win_start > target_pos), None)
            if split_at:
                segments.append((pos, split_at))
                pos = split_at
                continue
        segments.append((pos, pos + frag_len))
        pos += frag_len
    
    log_utils.info(f"Audio has been split into {len(segments)} segments")
    return segments

