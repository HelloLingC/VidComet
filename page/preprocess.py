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
    st.subheader('预处理')
    
    if not 'vid_file' in st.session_state:
        st.warning('视频文件未导入')
        return
    vid_file = st.session_state.vid_file
    st.text_input('视频文件', vid_file)
    log_placeholder = st.empty()
    log_utils.observable_handler.subscribe(update)
    if(st.button('开始', icon='🚀')):
        whisper_local.transcribe(vid_file)
        if os.path.exists(VOCAL_AUDIO_FILE_PATH):
            st.success('音频预处理成功！')
            st.text('人声部分：')
            st.audio(VOCAL_AUDIO_FILE_PATH)
        else:
            st.error('VOCAL FILE NOT EXISTED')
    
    st.subheader('转录')
    st.warning('请先进行音频预处理')

main()
# test()


    