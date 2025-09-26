import os
from . import log_utils
from utils.config_utils import *
import demucs.separate
import shlex

# or spleeter
def start_demucs():
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        log_utils.warn(f'File {VOCAL_AUDIO_FILE_PATH} already existed')
        # return
    log_utils.info('正在对音频进行人声分离...')
    # ig we need quote the audio path
    # mp3 bitrate default: 320
    # demucs will download model if not exists
    # !IMPORTANT process may be killed due to low GPU mem
    demucs.separate.main(shlex.split(f'--mp3 --two-stems=vocals -o \"{AUDIO_DIR}\" \"{RAW_AUDIO_FILE_PATH}\"'))
    log_utils.success('人声分离成功！')


if __name__ == '__main__':
    start_demucs()