import yaml
import os
import log_utils

AUDIO_DIR = os.path.join(os.getcwd(), 'output', 'audio')
RAW_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'raw.mp3')
VOCAL_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'htdemucs', 'raw', 'vocals.mp3')
BACKGROUND_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'no-vocals.mp3')
ENHANCED_VOCAL_PATH = os.path.join(AUDIO_DIR, 'enhanced-vocals.mp3')
COMPRESSED_AUDIO_PATH = os.path.join(AUDIO_DIR, 'compressed.mp3')
SEGMENT_TEMP_PATH = os.path.join(AUDIO_DIR, 'temp.mp3')

WHISPER_MODEL_DIR = os.path.join(os.getcwd(), 'models')

CONFIG_FILE_PATH = os.path.join(os.getcwd(),"config.yaml")

TRANSCRIPTION_PATH = os.path.join(os.getcwd(), 'output', 'transcript.csv')
TRANSCRIPTION_SENT_PATH = os.path.join(os.getcwd(), 'output', 'transcript_sent.csv')

SPLIT_LLM_PATH = os.path.join(os.getcwd(), 'output', 'split_llm.txt')

SRT_PATH = os.path.join(os.getcwd(), 'output', 'srt.srt')
SRT_TRANSLATION_PATH = os.path.join(os.getcwd(), 'output', 'srt_translation.srt')

# This function should be called in 'app.py'
# to get the current working directory. Don't let other moduless get cwd
def init_config_helper():
    if not os.path.exists(CONFIG_FILE_PATH):
        log_utils.warn('WARNING: Config file not found! Using empty config')
    
def get_config_value(keys:str):
    with open(CONFIG_FILE_PATH, 'r') as f:
        configs = yaml.safe_load(f)
    
    for key in keys.split('.'):
        if isinstance(configs, dict) and key in configs:
            configs = configs[key]
        else:
            raise KeyError(f'{key} not found in config file!')
    return configs