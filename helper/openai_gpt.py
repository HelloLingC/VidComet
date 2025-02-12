import openai
import log_utils
import config_utils
from json_repair import repair_json

def ask_gpt(prompt: str, response_json=True):
    api_url = config_utils.get_config_value('gpt.api_url')
    api_key = config_utils.get_config_value('gpt.api_key')
    model = config_utils.get_config_value('gpt.model')
    if not api_key :
        log_utils.error("API key is not set!")
        return None
    response = openai.ChatCompletion.create(
        api_url=api_url,
        api_key=api_key,
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    resp = response.choices[0].message["content"]
    if not response_json:
        return resp
    repair_json(resp)


if __name__ == "__main__":
    print(ask_gpt("What is the weather like today?"))
