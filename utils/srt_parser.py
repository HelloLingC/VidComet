import re
import sys
import os
import pandas as pd
# sys.path.append('./utils')
from . import config_utils as cfg

def parse_trans_and_ori_srt():
    """
    Return: original parsed srt and translated text from srt_trans
    """
    ori = parse_srt(cfg.SRT_PATH)
    trans = parse_srt(cfg.SRT_TRANS_PATH)
    texts = [item["text"] for item in trans]
    return ori, texts

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配每个字幕块
    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = int(lines[0])
            time_range = lines[1]
            text = '\n'.join(lines[2:])

            # 解析时间轴
            start_time, end_time = time_range.split(' --> ')
            subtitles.append({
                # 'index': index,
                'start_time': start_time.strip(),
                # 'end_time': end_time.strip(),
                'text': text.strip()
            })

    return subtitles