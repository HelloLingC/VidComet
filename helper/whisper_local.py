import whisperx
import torch
import log_utils
from config_utils import *
import subprocess
import librosa
import preprocess
import demucs_local

options_model = ["large-v2"]

# Preprocess video and transcribe audio via WhisperX
def transcribe(vid_file):
    # 0 音频轨道分离
    preprocess.convert_to_audio(vid_file)
    # 1 人声分离
    demucs_local.start_demucs()
    # 2 人声增强
    enhanced = preprocess.enhance_vocals()
    # 3 音频压缩
    preprocess.compress_audio(enhanced)
    # 4 音频切分
    preprocess.split_audio(COMPRESSED_AUDIO_PATH)
    # whisper转录
    transcribe_audio()

# set compute_type to "int8" if on low gpu mem
def transcribe_audio(device="cuda", model_arch="large-v2", compute_type='float16'):
    if(device == "cuda" and not torch.cuda.is_available()):
        log_utils.warn('GPU is not availablem, use CPU instead.')
        device = 'cpu'
    if device == 'cuda':
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        batch_size = 16 if gpu_mem > 8 else 2
        compute_type = "float16" if torch.cuda.is_bf16_supported() else "int8"
        log_utils.info(f'[GPU] Batch size: {batch_size}, compute_type: {compute_type}, gpu_mem: {gpu_mem}')
    else:
        batch_size = 1
        compute_type = 'int8'
        log_utils.info(f'[CPU] Batch size: {batch_size}, [cyan]compute_type: {compute_type}[/cyan]')
    cfg_lang = get_config_value('whisper.language')
    target_language = None if 'auto' in cfg_lang else cfg_lang
    vad_options = {"vad_onset": 0.500,"vad_offset": 0.363}
    asr_options = {"temperatures": [0],"initial_prompt": "",}
    model = whisperx.load_model(model_arch, device, compute_type=compute_type, language=target_language, vad_options=vad_options, asr_options=asr_options, download_root=WHISPER_MODEL_DIR)
    # Extract audio segment using ffmpeg
    ffmpeg_cmd = f'ffmpeg -y -i "{COMPRESSED_AUDIO_PATH}" -ss {start} -t {end-start} -vn -ar 32000 -ac 1 "{temp_audio_path}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True, capture_output=True)

    librosa.load()
