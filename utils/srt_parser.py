import re
import sys
import os
import config_utils as cfg

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
                'index': index,
                'start_time': start_time.strip(),
                'end_time': end_time.strip(),
                'text': text.strip()
            })

    return subtitles

# 使用示例
file_path = cfg.SRT_PATH
subtitles = parse_srt(file_path)
for sub in subtitles:
    print(f"Index: {sub['index']}")
    print(f"Time: {sub['start_time']} --> {sub['end_time']}")
    print(f"Text: {sub['text']}\n")