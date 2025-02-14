import log_utils
import pandas as pd
from config_utils import *

INPUT_FILE = ''
OUTPUT_SRT_FILE = ''

def _trim(s: str):
    """Delete all space str and dot punct"""
    # i dont know why, but replace func cannot remove space in
    # the sentence end, so need strip()
    return s.replace(' ', '').replace('.', '').strip()

def format_time(seconds):
    """将秒数转换为SRT时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def generate_srt(subtitles: list):
    with open(SRT_PATH, 'w', encoding='utf-8') as f:
        for i, (start_time, end_time, text) in enumerate(subtitles, start=1):
            # 写入序号
            f.write(f"{i}\n")
            # 写入时间轴
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            # 写入字幕文本
            f.write(f"{text}\n\n")

def get_sent_timestamp(df_words: pd.DataFrame, sents: list[str]):
    """
    df_words: 语音转录的单词表 每个word包含start, end, text
    df_sents: 需要进行时间轴对齐的句子
    """
    all_words_str = ''
    word_pos_index = {}
    # Build index for word query
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
        # code for debug
        # if i ==0:
        #     print(cleared_sent.strip())
        #     print(all_words_str[current_pos:current_pos+sent_len])
        #     print(len(cleared_sent))
        #     print(len(all_words_str[current_pos:current_pos+sent_len]))
        # interate all words till matched or meet the end
        while current_pos <= len(all_words_str) - len(sent):
            # print('current_pos: ' + all_words_str[current_pos:current_pos+sent_len])
            if all_words_str[current_pos:current_pos+sent_len] == cleared_sent:
                start_word_idx = word_pos_index[current_pos]
                end_word_idx = start_word_idx + sent_len - 1
                
                timestamp_list.append((
                    float(df_words['start'][start_word_idx]),
                    float(df_words['end'][end_word_idx]),
                    sent
                ))  
                
                current_pos += sent_len
                matched = True
                break
            current_pos += 1
        if not matched:
            log_utils.error('No match for sentence: ' + sent)
    print(timestamp_list)
    generate_srt(timestamp_list)

if __name__ == '__main__':
    with open(SPLIT_LLM_PATH, 'r') as f:
        df_sents = f.readlines()
    df = pd.read_csv(TRANSCRIPTION_PATH)
    get_sent_timestamp(df, df_sents)