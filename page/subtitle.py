import streamlit as st
from helper import log_utils

def update(msg):
    st.info(msg)

st.header('生成字幕')

log_utils.logger.attach(update)

if 'vid_file' in st.session_state:
    pass
