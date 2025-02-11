import yaml
import os

AUDIO_DIR = os.path.join(os.getcwd(), 'output', 'audio')
RAW_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'raw.mp3')
VOCAL_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'htdemucs', 'raw', 'vocals.mp3')
BACKGROUND_AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, 'no-vocals.mp3')
ENHANCED_VOCAL_PATH = os.path.join(AUDIO_DIR, 'enhanced-vocals.mp3')
COMPRESSED_AUDIO_PATH = os.path.join(AUDIO_DIR, 'compressed.mp3')

WHISPER_MODEL_DIR = os.path.join(os.getcwd(), 'models')

CONFIG_FILE_PATH = os.path.join(os.getcwd(),"config.yaml")

def set_config_value(keys:str, val):
    with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
        configs = yaml.safe_load(CONFIG_FILE_PATH)
    
def get_config_value(keys:str):
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
        configs = yaml.safe_load(CONFIG_FILE_PATH)
    
    for key in keys.split('.'):
        if isinstance(configs, dict) and key in configs:
            configs = configs[key]
        else:
            raise KeyError(f'{key} not found in config file!')
    return configs