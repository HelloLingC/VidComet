import requests
import config_utils as cfg

url = "https://api.siliconflow.cn/v1/audio/speech"

def start_tts():
    cfg.get_config_value('siliconflow.api_key')

payload = {
    "model": "fishaudio/fish-speech-1.5",
    "input": "The text to generate audio for",
    "voice": "fishaudio/fish-speech-1.5:alex",
    "response_format": "mp3",
    "sample_rate": 32000,
    "stream": True,
    "speed": 1,
    "gain": 0
}
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)