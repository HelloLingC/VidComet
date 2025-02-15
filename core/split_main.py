import pandas as pd
import spacy.cli
import spacy.cli.download
import log_utils
from config_utils import *
import env_check
import spacy
import split_comma
import split_llm

def prepare_spacy_model(lang):
    if lang == 'auto':
        lang = 'en'
    model_name = get_config_value(f'spacy.model_map.{lang}')
    try:
        nlp = spacy.load(model_name)
    except:
        log_utils.warn(f"Model {model_name} not found, downloading...")
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
    return nlp

def start_split(sents: list[str]=None):
    if env_check.is_gpu_available():
        spacy.prefer_gpu()
    else:
        log_utils.warn("GPU not available, using CPU.")

    lang = get_config_value('whisper.language')
    # if whisper.language set auto
    if lang == 'auto':
        lang = get_config_value('whisper.detected_language')

    with open(TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
    # temporarily use only llm splitter
    # for text in sents:
    #     t = split_comma.split_sent_by_comma(text, prepare_spacy_model(lang))
    splitter = split_llm.SplitterLLM(prepare_spacy_model(lang))
    splitter.split(sents)

def get_joiner(lang):
    if lang in get_config_value('language_space_joiner'):
        return " "
    elif lang in get_config_value('language_no_space_joiner'):
        return ""
    else:
        log_utils.error(f"Language {lang} not supported for joining.")
        return " "

if __name__ == '__main__':
    start_split()