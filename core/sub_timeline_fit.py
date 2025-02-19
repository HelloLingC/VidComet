import log_utils
import pandas as pd
from config_utils import *
import re
from difflib import SequenceMatcher

INPUT_FILE = ''
OUTPUT_SRT_FILE = ''

def _trim(s: str):
    """Delete all space str and dot punct"""
    # i dont know why, but replace func cannot remove space in
    # the sentence end, so need strip()
    # s = re.sub(r'\s+', ' ', s)
    # s = re.sub(r'[^\w\s]', '', s)
    # return s
    return s.replace(' ', '').replace('.', '').replace(',', '').replace('\"', '').replace('\n', '')

def format_time(seconds):
    """将秒数转换为SRT时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def generate_srt(subtitles: list):
    original = ""
    translation = ""
    for i, (start_time, end_time, text, trans) in enumerate(subtitles, start=1):
        # 写入序号
        original += f"{i}\n"
        translation += f"{i}\n"
        # 写入时间轴
        original += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        translation += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        # 写入字幕文本
        original += f"{text}\n\n"
        translation += f"{trans}\n\n"
    with open(SRT_PATH, 'w', encoding='utf-8') as f:
        f.write(original)
    with open(SRT_TRANS_PATH, 'w', encoding='utf-8') as f:
        f.write(translation)

def combine_sent_timestamp(df_words: pd.DataFrame, sents: list[str], t_sents: list[float]):
    """
    df_words: word matrix from whisper. Each word contains start, end, text
    sents: 需要进行时间轴对齐的句子
    t_sents: The translation of sentences (if have).
    """
    all_words_str = ''
    word_pos_index = {}
    # Build index for word query
    # the dict's key is added by each str's length
    # the value is the index of the word in df_words
    for i, word in df_words.iterrows():
        word = _trim(word['word'])
        word_pos_index[len(all_words_str)] = i
        all_words_str += word

    timestamp_list = []
    current_pos = 0
    for i, sent in enumerate(sents):
        matched = False
        cleared_sent = _trim(sent)
        sent_len = len(cleared_sent)

        # NOTICE: words table from whisper contain punct
        # But after LLM translation, it may disappear (like ',')
        # so the 'current_pos++' in this iteration end
        # make current_pos alwuys be right pos for next sentence
        while current_pos < len(all_words_str) - sent_len + 1:
            # print('current_pos: ' + all_words_str[current_pos:current_pos+sent_len])
            if SequenceMatcher(None, all_words_str[current_pos:current_pos+sent_len], cleared_sent).ratio() > 0.85:
                start_word_idx = word_pos_index[current_pos]
                # 'end_word_idx' point to the first word in the next sentence
                # so at the final sentence of text, end_word_idex point to None
                try:
                    end_word_idx = word_pos_index[current_pos + sent_len]
                except KeyError:
                    end_word_idx = len(df_words)
                timestamp_list.append((
                    float(df_words['start'][start_word_idx]),
                    float(df_words['end'][end_word_idx-1]),
                    sent,
                    t_sents[i] if t_sents else None
                ))

                current_pos += sent_len
                matched = True
                break
            # print("CUREENT++")
            # print("allwords: " + all_words_str[current_pos:current_pos+sent_len])
            current_pos += 1
        if not matched:
            print(cleared_sent)
            log_utils.error('No match for sentence: ' + cleared_sent)

    generate_srt(timestamp_list)

def start():
    with open(SPLIT_LLM_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
    with open(TRANS_LLM_PATH, 'r', encoding='utf-8') as f:
        t_sents = f.readlines()
    df_words = pd.read_csv(TRANSCRIPTION_PATH)
    combine_sent_timestamp(df_words, sents, t_sents)

if __name__ == '__main__':
    start()