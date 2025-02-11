import whisperx
import torch
import log_utils
import config_utils as cfg
import preprocess


options_model = ["large-v2"]

# Preprocess video and transcribe audio via WhisperX
def transcribe(vid_file):
    preprocess.convert_to_audio(vid_file)



# set compute_type to "int8" if on low gpu mem
def transcribe_audio(device, model_arch, compute_type='float16'):
    if(device == "cuda" and not torch.cuda.is_available()):
        device = 'cpu'
    if device == 'cuda':
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        batch_size = 16 if gpu_mem > 8 else 2
        compute_type = "float16" if torch.cuda.is_bf16_supported() else "int8"
    cfg_lang = cfg.get_config_value('whisper.language')
    target_language = None if 'auto' in cfg_lang else cfg_lang
    target_language = 'cn'
    model = whisperx.load_model(model_arch, device, compute_type=compute_type, language=target_language)
