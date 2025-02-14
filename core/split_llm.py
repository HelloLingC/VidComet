import concurrent.futures
import math
from config_utils import *
import split_main
import pandas
import gpt_openai
import gpt_prompts
import os

SPLIT_PATH: str = os.path.join(os.getcwd(), '/split_resp.txt')

def send_request(req):
    resp = gpt_openai.ask_gpt(f"{req}", gpt_prompts.get_split_prompt(10))
    if resp == None:
        # 如果LLM请求失败
        resp = req
    print('Catch Splitter LLM Response!')
    resp = resp.replace('<br>', '\n')
    resp = resp.replace('.', '\n')
    return resp


def split_by_llm(sents, nlp, num_threads: int=3):
    word_limit = 20
    unchanged_indexs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
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
                    future = executor.submit(send_request, pending_req)
                    futures.append(future)
                    pending_req = ""
            else:
                # 句子的单词数很小，无需拆分
                unchanged_indexs.append(i)
        # 处理剩余的请求
        if pending_req != "":
            future = executor.submit(send_request, pending_req)
        for future in futures:
            split_res = future.result()
            with open(os.getcwd() + '\\split_resp.txt', 'a') as f:
                f.write(split_res)
        # 将未被拆分的句子与已被拆分的句子合并
        with open(os.getcwd() + '\\split_resp.txt' , 'r') as file:
            lines = file.readlines()
        print(unchanged_indexs)
        for i in unchanged_indexs:
            # 在指定行插入文字
            lines.insert(i, sents[i].strip(' ').replace('.', '') + '\n')
        with open(os.getcwd() + '\\split_resp.txt' ,'w') as file:
            file.writelines(lines)

if __name__ == '__main__':
    df = pandas.read_csv(TRANSCRIPTION_SENT_PATH)
    nlp = split_main.prepare_spacy_model('en')
    split_by_llm(df['text'].tolist(), nlp)