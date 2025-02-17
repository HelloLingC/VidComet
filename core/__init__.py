from . import whisper_preprocess as preprocess
from . import demucs_local
from . import whisper_local
from . import config_utils as cfg

from enum import Enum
class CurrentState(Enum):
    VOCAL_SEPERATING = 1
    TRANSCRIBING = 2

def start_vocal_seperation(vid_path: str):
    """音频轨道分离 and vocal seperation"""
    preprocess.convert_to_audio(vid_path)
    demucs_local.start_demucs()

def start_asr():
    """Preprocess video and transcribe audio via WhisperX"""
    # 2 人声增强
    enhanced = preprocess.enhance_vocals()
    # 3 音频压缩
    preprocess.compress_audio(enhanced)
    # 4 音频切分
    segments = preprocess.split_audio(cfg.COMPRESSED_AUDIO_PATH)
    # whisper转录
    whisper_local.transcribe_segments(segments)