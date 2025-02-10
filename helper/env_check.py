import subprocess

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

def check_cuda():
    pass