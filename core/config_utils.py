import ruamel.yaml
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

# Whisper transcription word by word
TRANSCRIPTION_PATH = os.path.join(os.getcwd(), 'output', 'transcript.csv')
# Whisper transcription but only sentences without timeline
TRANSCRIPTION_SENT_PATH = os.path.join(os.getcwd(), 'output', 'transcript_sent.csv')

SPLIT_LLM_PATH = os.path.join(os.getcwd(), 'output', 'split_llm.txt')
TRANSLATE_LLM_PATH = os.path.join(os.getcwd(), 'output', 'tranlated_llm.txt')

SRT_PATH = os.path.join(os.getcwd(), 'output', 'srt.srt')
SRT_TRANSLATION_PATH = os.path.join(os.getcwd(), 'output', 'srt_translation.srt')

# This function should be called in 'app.py'
# to get the current working directory. Don't let other moduless get cwd
def init_config_helper():
    if not os.path.exists(CONFIG_FILE_PATH):
        log_utils.warn('WARNING: Config file not found! Using empty config')
    
def get_config_value(keys:str):
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
        yaml = ruamel.yaml.YAML(typ='rt')
        configs = yaml.load(f)
    
    for key in keys.split('.'):
        if isinstance(configs, dict) and key in configs:
            configs = configs[key]
        else:
            raise KeyError(f'{key} not found in config file!')
    return configs

# Todo: create a new column
def set_config_value(key_str: str, value: str):
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
        yaml = ruamel.yaml.YAML(typ='rt')
        configs = yaml.load(f)

    if not isinstance(configs, dict):
        print('ERROR: Config file is not a dictionary!')
        return
    keys = key_str.split('.')
    current = configs
    for k in keys[:-1]:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return False

    if isinstance(current, dict) and keys[-1] in current:
        current[keys[-1]] = value
        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as file:
            yaml.dump(configs, file)
        return True
    else:
        raise KeyError(f"Key '{keys[-1]}' not found in configuration")

if __name__ == '__main__':
    set_config_value('whisper.lal', 'a')