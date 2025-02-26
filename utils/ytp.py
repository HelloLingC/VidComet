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

def download(url, res, cookie_file=None):
    parsed_res = parse_res(res)
    # Make sure -S is after -o
    cmd = ['yt-dlp', "-o", f"{saved_path}", "--cookies", f"{cookie_file}"
            , "-S", f"{parsed_res}", f'{url}']

     # Add cookies option only if file exists
    if cookie_file and os.path.exists(cookie_file):
        cmd.extend(["--cookies", cookie_file])
    cmd.append(url)  # Add URL at the end

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"Error output: {e.stderr}")