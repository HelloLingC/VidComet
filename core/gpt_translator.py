import concurrent.futures
import gpt_openai
import gpt_prompts
import json
import json_repair
from config_utils import *
import log_utils

"""
在splir_llm后, 根据LLM切分的字幕进行翻译
"""
handled_batch_num = 0
conversation_history = []

def pack_json_req(texts: list) -> str:
    """
    Packs a list of text strings into a JSON format with numbered keys.
    Args:
        texts (list): List of text strings to be packed into JSON
    Returns:
        str: JSON string with numbered keys (1-based) mapping to text values
    """
    reqs = {}
    for i, text in enumerate(texts, start=1):
        reqs[str(i)] = text
    return json.dumps(reqs)

def write_result(res: str) -> dict:
    # Something wrong when asking gpt
    if(res == None):
        return
    obj = json_repair.repair_json(res, return_objects=True)
    lines = [obj[key]['revised_translation'] + '\n' for key in obj]
    with open(TRANS_LLM_PATH, 'a', encoding='utf-8') as f:
        f.writelines(lines)

def translate(pending_reqs: list) -> str:
    global conversation_history
    if len(conversation_history) > 2:
        conversation_history = conversation_history[-2:]

    chunk = pack_json_req(pending_reqs)
    conversation_history.append({'role': 'user', 'content': chunk})
    res = gpt_openai.ask_gpt(chunk, system_prompt=gpt_prompts.get_translation_prompt(), conversation_history=conversation_history)
    if res != None:
        conversation_history.append({'role': 'assistant', 'content': res})
    else:
        conversation_history.pop()
    return res

def start_translate(sents: tuple=None, num_threads=3, batch_size=8):
    if os.path.exists(TRANS_LLM_PATH):
        log_utils.warn('Deleted existed translation file.')
        os.remove(TRANS_LLM_PATH)
    if sents == None:
        with open(SPLIT_LLM_PATH, 'r', encoding='utf-8') as f:
            sents = f.readlines()
    import gpt_summary
    gpt_summary.start_summary()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        pending_reqs = []
        futures = []
        handled_batch_num = 0
        for i, sent in enumerate(sents):
            # 每条句子总是以\n结尾
            sent = sent.replace('\n', '')
            pending_reqs.append(sent)
            if len(pending_reqs) >= batch_size:
                handled_batch_num += 1
                log_utils.info(f'{handled_batch_num} Batch: Translating {len(pending_reqs)} sentences...')
                futures.append(executor.submit(translate, pending_reqs))
                pending_reqs = []
        if pending_reqs:
            futures.append(executor.submit(translate, pending_reqs))
        for future in futures:
            result = future.result()
            write_result(result)

if __name__ == '__main__':
    start_translate()