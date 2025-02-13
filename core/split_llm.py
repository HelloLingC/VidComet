from concurrent.futures import ThreadPoolExecutor, as_completed
import math
from config_utils import *
import split_main
import pandas
import gpt_openai
import gpt_prompts
import os

def send_request(req):
    resp = gpt_openai.ask_gpt(f"{req}", gpt_prompts.get_split_prompt(10))
    resp = resp.replace('<br>', '\n')
    resp = resp.replace('.', '\n')
    with open(os.getcwd() +'/split_resp.txt', 'a') as f:
        f.write(resp)
    # for req in reqs:
    #     print(req['s'])
    #     resp = gpt_openai.ask_gpt(f"{req['s']}", gpt_prompts.get_split_prompt(req['n'], 20))
    #     print(resp)

def split_by_llm(sents, nlp, num_threads: int=3):
    word_limit = 20
    result = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        pending_req = ""
        for i, sent in enumerate(sents):
            sent = sent.strip()
            # 一条句子的单词数
            word_count = len(nlp(sent))
            # 如果单词数大于阈值，则进行拆分
            if word_count > word_limit:
                # 需要拆分的分段数
                part_num = math.ceil(word_count / word_limit)
                pending_req = f'{pending_req}\n{sent}'
                # print(pending_req)
                if len(pending_req) >= 3:
                    executor.submit(send_request, pending_req)
                    pending_req = ""
            else:
                # 句子的单词数很小，无需拆分
                result.append(i)
        # 处理剩余的请求
        if pending_req:
            executor.submit(send_request, pending_req)

if __name__ == '__main__':
    
    # with open(TRANSCRIPTION_SENT_PATH, 'r') as file:
    #     split_by_llm(file.readlines(), nlp)
    df = pandas.read_csv(TRANSCRIPTION_SENT_PATH)
    nlp = split_main.prepare_spacy_model('en')
    split_by_llm(df['text'].tolist(), nlp)