import streamlit as st
import core.config_utils as cfg
import core.split_main as split
import core.gpt_translator
import core.log_utils
import core.sub_timeline_fit

log_placeholder = None
msg_arr = ''
def update(msg: str):
    global msg_arr
    msg_arr += '\n'*3 + msg
    log_placeholder.info(msg_arr)

def main():
    global log_placeholder
    st.header('字幕切分')

    core.log_utils.observable_handler.subscribe(update)
    log_placeholder = st.empty()

    if(st.button('LLM 切分')):
        split.start_split()
        if(st.button('开始翻译')):
            core.gpt_translator.start_translate()
            st.success('翻译完成')
    if(st.button('开始翻译')):
        core.gpt_translator.start_translate()
        st.success('翻译完成')
    if(st.button('双语字幕生成')):
        core.sub_timeline_fit.start()
        st.success('完成')
    if not 'step' in st.session_state or st.session_state.step != 3:
        st.warning('请先完成前一步骤')
        return

main()