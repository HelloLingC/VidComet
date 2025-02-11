import streamlit as st
from helper import log_utils, whisper_local

def update(msg):
    st.info(msg)

def main():
    st.header('生成字幕')
    log_utils.observable_handler.subscribe(update)
    if not 'vid_file' in st.session_state:
        st.warning('视频文件未导入')
        return
    vid_file = st.session_state.vid_file
    st.text_input('视频文件', vid_file)
    whisper_local.transcribe(vid_file)

main()


    