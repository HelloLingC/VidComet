import config_utils as cfg
import gpt_openai
import gpt_prompts
import os

def start_summary():
    if(not os.path.exists(cfg.TRANSCRIPTION_SENT_PATH)):
        print("TRANSSCRIPTION_SENT_PATH file not existed")
        return
    with open(cfg.TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
        res = gpt_openai.ask_gpt("".join(sents), gpt_prompts.get_summary_prompt(), response_json=True)
        with open(cfg.SUMMARY_PATH, 'w', encoding='utf-8') as f:
            f.write(res)

if __name__ == '__main__':
    start_summary()