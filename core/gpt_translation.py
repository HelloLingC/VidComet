import concurrent.futures
import gpt_openai
import gpt_prompts

"""
在splir_llm后, 根据LLM切分的字幕进行翻译
"""


def translate():
    gpt_openai.ask_gpt("", system_prompt=gpt_prompts.get_translation_prompt())

def start_translate(sents: tuple, num_threads=4, batch_size=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(translate, sents)