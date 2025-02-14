import concurrent.futures
import gpt_openai
import gpt_prompts
import json
import json_repair
from config_utils import *

"""
在splir_llm后, 根据LLM切分的字幕进行翻译
"""

def pack_json_req(texts: list) -> str:
    reqs = {}
    for i, text in enumerate(texts, start=1):
        reqs[str(i)] = text
    return json.dumps(reqs)

def write_result(res: str) -> dict:
    obj = json_repair.repair_json(res, return_objects=True)
    lines = [obj[key]['revised_translation'] + '\n' for key in obj]
    with open(TRANSLATE_LLM_PATH, 'a', encoding='utf-8') as f:
        f.writelines(lines)

def translate(pending_reqs: list) -> str:
    chunk = pack_json_req(pending_reqs)
    res = gpt_openai.ask_gpt(chunk, system_prompt=gpt_prompts.get_translation_prompt())
    return res

def start_translate(sents: tuple, num_threads=3, batch_size=8):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        pending_reqs = []
        futures = []
        for i, sent in enumerate(sents):
            # 每条句子总是以\n结尾
            sent = sent.replace('\n', '')
            pending_reqs.append(sent)
            if len(pending_reqs) >= batch_size:
                futures.append(executor.submit(translate, pending_reqs))
                pending_reqs = []
        if pending_reqs:
            futures.append(executor.submit(translate, pending_reqs))
        for future in futures:
            result = future.result()
            write_result(result)

if __name__ == '__main__':
    with open(SPLIT_LLM_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
    start_translate(sents[0:4])