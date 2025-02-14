from openai import OpenAI
import log_utils
import config_utils
from json_repair import repair_json

DEFAULT_SYSTEM_PROMPT = "you are a helpful, knowledgeable AI assistant."

def ask_gpt(prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT, response_json=False):
    api_url = config_utils.get_config_value('gpt.api_url')
    api_key = config_utils.get_config_value('gpt.api_key')
    model = config_utils.get_config_value('gpt.model')
    if not api_url:
        log_utils.error("API URL is not set!")
        return None
    if not api_key:
        log_utils.error("API key is not set!")
        return None
    
    client = OpenAI(api_key=api_key, base_url=api_url, max_retries=3)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        resp = response.choices[0].message.content
    except Exception as e:
        log_utils.error(f"Error while asking GPT: {e}")
        return None
    if not response_json:
        return resp
    return repair_json(resp)


if __name__ == "__main__":
    print(ask_gpt("What is the weather like today?"))
