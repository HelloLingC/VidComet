import streamlit as st
from core import log_utils, whisper_local
from core.config_utils import *
import os
import pandas as pd

log_placeholder = None
msg_arr = ''
def update(msg):
    global msg_arr
    msg_arr += '\n'*3 + msg
    log_placeholder.info(msg_arr)

def start_transcribe():
    vid_file = st.session_state.vid_file
    whisper_local.transcribe(vid_file)
    if os.path.exists(VOCAL_AUDIO_FILE_PATH):
        st.session_state.step = 3
        st.success('音频预处理成功！')
        st.text('人声部分：')
        st.audio(VOCAL_AUDIO_FILE_PATH)
    else:
        st.error('VOCAL FILE NOT EXISTED')

def main():
    tab = st.tabs(['预处理', '配置'])
    with tab[0]:
        pass

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
    if 'step' in st.session_state:
        st.button('开始', icon='🚀', on_click=start_transcribe)
    else:
        st.subheader('转录')
        st.button('下一步', use_container_width=True)
        st.dataframe(pd.read_csv(TRANSCRIPTION_SENT_PATH))

main()

    