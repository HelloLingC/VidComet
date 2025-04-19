import concurrent.futures
import math
from utils.config_utils import *
import log_utils
import gpt_openai
import gpt_prompts

class SplitterLLM:
    def __init__(self, nlp):
        self.sents: list[str] = None
        self.nlp = nlp
        self.handled_batch_num = 0

    def send_request(self, req, part_num, unchanged_indexs):
        resp = gpt_openai.ask_gpt(f"{req}", gpt_prompts.get_split_prompt(10))
        # LLM request failed
        if resp == None:
            print('Something wrong when asking gpt')
            resp == req         
        print('Catch Splitter LLM Response for a batch!')
        resp = resp.replace('<br>', '\n')
        resp = resp.replace('.', '\n')
        for i in unchanged_indexs:
            resp = f'{self.sents[i]}{resp}'
        return resp

    def split(self, sents: list[str], num_threads: int=3, batch_size: int=5):
        """
        nlp: Spacy model
        """
        self.sents = sents
        word_limit = 12
        unchanged_indexs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            pending_req = []
            for i, sent in enumerate(sents):
                sent = sent.strip()
                # the word count of a sentence by nlp
                word_count = len(self.nlp(sent))
                # 如果单词数大于阈值，则进行拆分
                if word_count > word_limit:
                    # 需要拆分的分段数
                    # 'sent' already has the line separator
                    part_num = math.ceil(word_count / word_limit)
                    pending_req.append(sent)
                    if len(pending_req) >= batch_size:
                        self.handled_batch_num += 1
                        log_utils.info(f'{self.handled_batch_num} Batch: Splitting {len(pending_req)} sentences...')
                        future = executor.submit(self.send_request, pending_req, part_num, unchanged_indexs)
                        futures.append(future)
                        pending_req = []
                else:
                    # 句子的单词数很小，无需拆分
                    # Store its index, let next pending request carry it
                    unchanged_indexs.append(i)

            # Handle the remaining sentences
            if pending_req:
                future = executor.submit(self.send_request, pending_req)
                futures.append(future)
            split_results = []
            for future in futures:
                fu_res = future.result()
                split_results.append(fu_res)

            # 将未被拆分的句子与已被拆分的句子合并
            # Since insertion will alter the indices
            # need to insert in reverse order
            # for i in reversed(unchanged_indexs):
            #     print(f'Inserting {sents[i]} at {i}')
            #     # 在指定行插入文字
            #     split_results.insert(i, sents[i].strip(' ').replace('.', ''))
            with open(SPLIT_LLM_PATH,'w') as file:
                file.writelines(split_results)
