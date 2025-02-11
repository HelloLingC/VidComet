import os
import log_utils
from config_utils import *
import demucs.separate
import shlex

def start_demucs():
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        log_utils.info(f'File {VOCAL_AUDIO_FILE_PATH} already existed')
        return
    # ig we need quote the audio path
    # mp3 bitrate default: 320
    demucs.separate.main(shlex.split(f'--mp3 --two-stems=vocals \"{RAW_AUDIO_FILE_PATH}\"'))
    log_utils.success('')

    