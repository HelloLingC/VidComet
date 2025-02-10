import whisperx
import torch

options_model = ["large-v2"]

# set compute_type to "int8" if on low gpu mem
def transcribe_audio(device, model_arch, compute_type='float16'):
    if(device == "cuda" and not torch.cuda.is_available()):
        device = 'cpu'
    if device == 'cuda':
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        batch_size = 16 if gpu_mem > 8 else 2
        compute_type = "float16" if torch.cuda.is_bf16_supported() else "int8"
    target_language = "cn"
    model = whisperx.load_model(model_arch, device, compute_type=compute_type, language=target_language)
