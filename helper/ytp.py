import subprocess
import os

saved_path = os.path.join(os.getcwd(), "downloads", "%(title)s-%(id)s.%(ext)s")

def parse_res(res):
    if(res == '最高画质'):
        return 'ext' # best video with best ext
    if(res == '最低画质'):
        return '+size,+br'
    else:
        return f"res:{res.replace('p', '')}"

def download(url, res, output_path=saved_path):
    parsed_res = parse_res(res)
    print(parsed_res)
    print(url)
    print(output_path)
    try:
        # Make sure -S is after -o
        cmd = ['yt-dlp', "-o", f"{output_path}"
               , "-S", f"{parsed_res}", f'{url}']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"Error output: {e.stderr}")
    
