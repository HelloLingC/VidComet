import streamlit as st
from core import log_utils, whisper_local, demucs_local
from core.config_utils import *
import os
import builtins

old_print = builtins.print

def hook_print():
    def hook(*args, **kwargs):
        old_print("lol", end='')
        old_print(*args, **kwargs)
        update(" ".join(args))
    builtins.print = hook

def unhook_print():
    builtins.print = old_print

st_progress = None
progress = 0
def update(msg):
    global progress
    progress += 1
    # st_progress.progress(progress / 30, "Processing...")
    st_progress.status(msg)

def check_whisper_models():
    pass

st_asr_result = None
def start_asr():
    demucs_local.start_demucs()
    st_asr_result.success('人声分离成功！')
    st_asr_result.markdown(f'结果保存在 `{VOCAL_AUDIO_FILE_PATH}`')
    st_asr_result.audio((VOCAL_AUDIO_FILE_PATH))

st_trans_result = None
def start_transcribe():
    vid_file = st.session_state.vid_file
    # process = subprocess.Popen(['python', 'core/whisper_local.py', vid_file], stdout=subprocess.PIPE)
    # hook_print()
    whisper_local.transcribe(vid_file)
    # unhook_print()
    # while True:
    #     output = process.stdout.readline()
    #     if output == '' and process.poll() is not None:
    #         break
    #     if output:
    #         print(output.strip())
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        st.session_state.step = 3
        st_trans_result.success('音频转录成功！')
        st_trans_result.markdown(f'结果保存在 `{TRANSCRIPTION_SENT_PATH}`')
        st_trans_result.write(open(TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8'))
    else:
        st_trans_result.error('VOCAL FILE NOT EXISTED')

def main():
    global st_trans_result
    global st_asr_result
    global st_progress

    st.header('🎧语音识别')
    tab = st.tabs(['主页', '配置'])
    with tab[0]:
        pass

    st.session_state.vid_existed = 'vid_file' in st.session_state
    if st.session_state.vid_existed:
        vid_file = st.session_state.vid_file
        origin_path = st.text_input('视频文件', vid_file)
    else:
        origin_path = st.text_input('视频文件', '')

    if origin_path == '':
        st.error('视频文件路径不能为空！')

    with st.container(border=True):
        st.subheader('人声分离')
        st.selectbox('模型', ['htdemucs', 'htdemucs-ft', 'htdemucs_6s', 'mdx_extra_q'])
        st_progress = st.empty()
        st.button("开始", icon='🚀', on_click=start_asr, disabled=(origin_path == ''))
        st_asr_result = st.container()

    with st.container(border=True):
        st.subheader('语音识别')
        cols = st.columns(2)
        cols[0].selectbox('选择模型', ['large-v3-turbo', 'large-v2', 'large-v3'])
        cols[1].selectbox('目标语言', ['自动检测', 'English', '中文'])
        st_progress = st.empty()
        st.button("开始转录", icon='🚀', on_click=start_transcribe, disabled=(origin_path == ''))
        st_trans_result = st.container()


    log_utils.observable_handler.subscribe(update)
    # if not 'step' in st.session_state:
    #     st.button('开始', icon='🚀', on_click=start_transcribe)
    # else:
    #     if(st.button('下一步', icon='🚀')):
    #         st.switch_page('page/splitter.py')
    #     st.write('语音识别: ', open(TRANSCRIPTION_SENT_PATH, 'r').readlines())


main()

