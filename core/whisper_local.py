import whisperx
import torch
import gc
import log_utils
from config_utils import *
import subprocess
import whisper_preprocess as preprocess
import shlex
# import librosa
import core.whisper_preprocess as whisper_preprocess
import sys
import pandas as pd

options_model = ["large-v3"]

# Preprocess video and transcribe audio via WhisperX
def transcribe(vid_file):
    # 0 音频轨道分离
    preprocess.convert_to_audio(vid_file)
    # 1 人声分离
    # demucs_local.start_demucs()
    # 2 人声增强
    enhanced = preprocess.enhance_vocals()
    # 3 音频压缩
    preprocess.compress_audio(enhanced)
    # 4 音频切分
    segments = whisper_preprocess.split_audio(COMPRESSED_AUDIO_PATH)
    # whisper转录
    transcribe_segments(segments)

"""transcribe audio segememts one by one"""
def transcribe_segments(segments):
    texts = []
    result = []
    for start, end in segments:
        log_utils.info(f"正在转录片段 从 {start} 到 {end} 秒")
        res = transcribe_audio(start, end)
        for segment in res['segments']:
            # transcribed text from Whisperx always with inappropriate quotes 
            text = segment['text'].strip("\"").strip(" ")
            # for sententces, we don't need timeline
            # texts.append({'start': segment['start'], 'end': segment['end'], 'text': text})
            texts.append(text + '\n')
            # words prop is a word list
            result.extend(segment['words'])
    df = pd.DataFrame(result)
    df.to_csv(TRANSCRIPTION_PATH, index=False)
    with open(TRANSCRIPTION_SENT_PATH, 'w', encoding='utf-8') as f:
        # writelines won't add a line seperator after each line
        f.writelines(texts)

# set compute_type to "int8" if on low gpu mem
def transcribe_audio(start: float, end: float, device="cuda", compute_type='float16') -> dict:
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
    log_utils.info('开始进行语音识别...')
    cfg_lang = get_config_value('whisper.language')
    model_arch = get_config_value('whisper.model')
    cfg_lang = 'auto'
    target_language = None if 'auto' in cfg_lang else cfg_lang
    vad_options = {"vad_onset": 0.500,"vad_offset": 0.363}
    asr_options = {"temperatures": [0],"initial_prompt": "",}
    model = whisperx.load_model(model_arch, device, compute_type=compute_type, language=target_language, vad_options=vad_options, asr_options=asr_options, download_root=WHISPER_MODEL_DIR)
    # Extract audio segment using ffmpeg
    ffmpeg_cmd = f'ffmpeg -y -i "{COMPRESSED_AUDIO_PATH}" -ss {start} -t {end-start} -vn -ar 32000 -ac 1 "{SEGMENT_TEMP_PATH}"'
    # on Windows, it seems like use shell=True sometimes return exit code 1
    # use shlex.split() to avoid this
    subprocess.run(shlex.split(ffmpeg_cmd), check=True, capture_output=True)

    # segment, sample_rate = librosa.load(SEGMENT_TEMP_PATH, sr=16000)
    segment = whisperx.load_audio(SEGMENT_TEMP_PATH, 16000)

    result = model.transcribe(segment, batch_size, print_progress=True)
    log_utils.success('🎉转录成功！')

    set_config_value('whisper.detected_language', result['language'])

    os.unlink(SEGMENT_TEMP_PATH)
    gc.collect()
    del model
    torch.cuda.empty_cache()

    # Align whisper output :)
    model_a, metadata = whisperx.load_align_model(language_code=result['language'], device=device)
    result = whisperx.align(result['segments'], model_a, metadata, segment, device, return_char_alignments=False)
    log_utils.success('对齐成功！')

    gc.collect()
    del model_a
    torch.cuda.empty_cache()

    # Since this function may process multiple segments,
    # the starting point of each segment is considered as 0s by Whisper.
    # However, in fact, the segments are processed in order.
    
    return result

if __name__ == '__main__':
    transcribe(sys.argv[1])