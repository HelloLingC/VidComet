import streamlit as st
import os
import core.config_utils as cfg

def main():
    st.header('Video Preview')
    if os.path.exists(cfg.OUTPUT_VIDEO):
        st.video(cfg.OUTPUT_VIDEO)
    else:
        st.error('视频文件不存在')

main()