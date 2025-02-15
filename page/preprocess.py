import streamlit as st
from core import log_utils, whisper_local
from core.config_utils import *
import os
import pandas as pd

log_placeholder = None
progress_placeholder = None
progress = 0
msg_arr = ''
def update(msg):
    global progress
    global msg_arr
    progress += 1
    progress_placeholder.progress(progress / 30, "Processing...")
    msg_arr += '\n'*3 + msg
    log_placeholder.info(msg_arr)

result_placeholder = None
def start_transcribe():
    vid_file = st.session_state.vid_file
    whisper_local.transcribe(vid_file)
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        st.session_state.step = 3
        result_placeholder.success('音频预处理成功！')
        result_placeholder.text('人声部分：')
        result_placeholder.audio(VOCAL_AUDIO_FILE_PATH)
    else:
        st.error('VOCAL FILE NOT EXISTED')

def main():
    global log_placeholder
    global progress_placeholder
    global result_placeholder

    st.header('🎧语音识别')
    tab = st.tabs(['预处理', '配置'])
    with tab[0]:
        pass
    st.subheader('预处理')

    if not 'vid_file' in st.session_state:
        st.warning('视频文件未导入')
        return
    vid_file = st.session_state.vid_file
    log_placeholder = st.empty()
    progress_placeholder = st.empty()
    result_placeholder = st.container().empty()
    log_utils.observable_handler.subscribe(update)
    if not 'step' in st.session_state:
        st.text_input('视频文件', vid_file)
        st.button('开始', icon='🚀', on_click=start_transcribe)
    else:
        if(st.button('下一步', icon='🚀')):
            st.switch_page('page/splitter.py')
        st.write('语音识别: ', open(TRANSCRIPTION_SENT_PATH, 'r').readlines())


main()

