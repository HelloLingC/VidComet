import streamlit as st
import core.config_utils as cfg
import core.split_main as split
import core.gpt_translator
import core.log_utils

log_placeholder = None
msg_arr = ''
def update(msg: str):
    global msg_arr
    msg_arr += '\n'*3 + msg
    log_placeholder.info(msg_arr)

def main():
    global log_placeholder
    st.header('字幕切分')

    with open(cfg.TRANSCRIPTION_SENT_PATH, 'r', encoding='utf-8') as f:
        sents = f.readlines()
    st.write(sents)

    core.log_utils.observable_handler.subscribe(update)
    log_placeholder = st.empty()

    if(st.button('LLM 切分')):
        split.start_split(sents)
        if(st.button('开始翻译')):
            core.gpt_translator.start_translate()
            st.success('翻译完成')
    if not 'step' in st.session_state or st.session_state.step != 3:
        st.warning('请先完成前一步骤')
        return

main()