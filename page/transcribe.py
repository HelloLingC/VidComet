import streamlit as st
import core.config_utils as cfg
import core.split_main as split

st.header('字幕切分')

def main():
    with open(cfg.TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
    split.start_split(sents)
    if not 'step' in st.session_state or st.session_state.step != 3:
        st.warning('请先完成前一步骤')
        return

main()