from concurrent.futures import ThreadPoolExecutor, as_completed
import math
import gpt_openai
import gpt_prompts

def send_request(req):
    for sent, part_num in req:
        gpt_openai.ask_gpt(f"{sent}", gpt_prompts.get_split_prompt(part_num, 20))

def split():
    pass

def split_by_llm(sents, nlp, num_threads: int=3):
    word_limit = 20
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        pending_req = []
        for i, sent in sents:
            # 一条句子的单词数
            word_count = len(nlp(sent))
            # 如果单词数大于阈值，则进行拆分
            if word_count > word_limit:
                # 需要拆分的分段数
                part_num = math.ceil(word_count / word_limit)
                pending_req.append((sent, part_num))
                if len(pending_req) >= 5:
                    executor.submit(send_request, pending_req)
        # 处理剩余的请求
        if pending_req:
            executor.submit(send_request, pending_req)