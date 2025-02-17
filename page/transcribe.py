import streamlit as st
from core import log_utils
import core
from core import config_utils as cfg
import os
import builtins

old_print = builtins.print

def hook_print():
    def hook(*args, **kwargs):
        update(' '.join(map(str,args)))
    builtins.print = hook

def unhook_print():
    builtins.print = old_print

st_progress = None
st_trans_progress = None
def update(msg):
    if st.session_state.state == core.CurrentState.VOCAL_SEPERATING:
        st_progress.status(msg)
    else:
        st_trans_progress.status(msg)

def check_whisper_models():
    pass

def main():
    global st_progress
    global st_trans_progress

    st.header('🎧语音识别')

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
        st_asr_result = st.container()
        if(st.button("开始", icon='🚀', disabled=(origin_path == ''))):
            st.session_state.state = core.CurrentState.VOCAL_SEPERATING
            core.start_vocal_seperation(origin_path)
            st_progress.status("人声分离成功！",  state='complete')
            st_asr_result.markdown(f'结果保存在 `{cfg.VOCAL_AUDIO_FILE_PATH}`')
            st_asr_result.audio((cfg.VOCAL_AUDIO_FILE_PATH))

    with st.container(border=True):
        st.subheader('语音识别')
        cols = st.columns(2)
        cols[0].selectbox('选择模型', ['large-v3-turbo', 'large-v2', 'large-v3'])
        cols[1].selectbox('目标语言', ['自动检测', 'English', '中文'])
        st_trans_progress = st.empty()
        st_trans_result = st.container()
        if st.button("开始转录", icon='🚀', disabled=(origin_path == '')):
            st.session_state.state = core.CurrentState.TRANSCRIBING
            hook_print()
            core.start_asr()
            unhook_print()
            if os.path.exists(cfg.VOCAL_AUDIO_FILE_PATH):
                st_trans_progress.status("语音转录成功！",  state='complete')
                st_trans_result.markdown(f'结果保存在 `{cfg.TRANSCRIPTION_SENT_PATH}`')
            else:
                st_trans_result.error('VOCAL FILE NOT EXISTED')

    log_utils.observable_handler.subscribe(update)

main()

