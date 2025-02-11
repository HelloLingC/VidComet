import streamlit as st
from helper import log_utils, whisper_local
from helper.config_utils import *
import os

log_placeholder = None
msg_arr = ''
def update(msg):
    global msg_arr
    msg_arr += '\n'*3 + msg
    log_placeholder.info(msg_arr)

def test():
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        st.audio(VOCAL_AUDIO_FILE_PATH)

def main():
    global log_placeholder
    st.header('生成字幕')
    
    if not 'vid_file' in st.session_state:
        st.warning('视频文件未导入')
        return
    vid_file = st.session_state.vid_file
    st.text_input('视频文件', vid_file)
    log_placeholder = st.empty()
    log_utils.observable_handler.subscribe(update)
    if(st.button('start')):
        whisper_local.transcribe(vid_file)
        if os.path.exists(VOCAL_AUDIO_FILE_PATH):
            st.text('人声部分：')
            st.audio(VOCAL_AUDIO_FILE_PATH)
        else:
            st.error('VOCAL FILE NOT EXISTED')

main()
# test()


    