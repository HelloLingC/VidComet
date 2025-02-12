import subprocess
import torch

def check_torch_cuda():
    print("Torch version:", torch.__version__)
    print("CUDA version:", torch.version.cuda)
    print("cuDNN version:", torch.backends.cudnn.version())
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("CUDA device:", torch.cuda.get_device_name(torch.cuda.current_device()))
    else:
        print("CUDA not available")

# if ffmpeg exists return ffmpeg version
# else, return None
def check_ffmpeg():
    try:
        res = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # ffmpeg is installed
        if res.returncode == 0:
            version_line = res.stdout.splitlines()[0]
            version = version_line.split()[2]
            return version
    except FileNotFoundError:
        print('ERR')
        return None
    return None

if __name__ == "__main__":
    check_torch_cuda()