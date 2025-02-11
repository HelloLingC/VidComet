import openai
import log_utils
import config_utils

def ask_gpt(prompt: str, model="gpt-3.5-turbo"):
    api_url = config_utils.get_config_value('gpt.api_url')
    api_key = config_utils.get_config_value('gpt.api_key')
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
    return response.choices[0].message["content"]
