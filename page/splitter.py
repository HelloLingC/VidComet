import streamlit as st
import sys, os
sys.path.append(os.getcwd() +'/core')
from core import config_utils as cfg
import core.split_main
import core.gpt_translator
from core import log_utils
import core.sub_timeline_fit

log_placeholder = None
def update(msg: str):
    log_placeholder.status(msg)

def main():
    sys.path.append(os.getcwd() +'/core')
    global log_placeholder
    st.header('字幕 Subtitle')

    model = cfg.get_config_value('gpt.model')
    core.log_utils.observable_handler.subscribe(update)
    log_placeholder = st.empty()

    with st.container(border=True):
        st.subheader('切分')
        st.text_input('LLM 模型', model)
        if(st.button('LLM 切分')):
            core.split_main.start_split()
            st.success('切分成功')

    with st.container(border=True):
        st.subheader('翻译')
        st.text_input('LLM 翻译模型', model)
        st.checkbox('专家模式')
        if(st.button('开始翻译')):
            core.gpt_translator.start_translate()
            st.success('翻译完成')

    with st.container(border=True):
        st.subheader('时间轴')
        cols = st.columns(2)
        cols[0].color_picker("翻译字幕颜色", "#FFFFFF")
        cols[1].color_picker("字幕颜色", "#FFFFFF")
        if(st.button('双语字幕生成')):
            core.sub_timeline_fit.start()
            st.success('完成')

main()