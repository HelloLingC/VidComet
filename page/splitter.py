import streamlit as st
import sys, os
sys.path.append(os.getcwd() +'/core')
from core import config_utils as cfg
from core import log_utils
import core.split_main
import core.gpt_translator
import core.sub_timeline_fit

split_status = None
translate_status = None
subtitles_status = None
def update(msg: str):
    if st.session_state.state == core.CurrentState.LLM_SPILITTING:
        split_status.status(msg)
        return
    elif st.session_state.state == core.CurrentState.TRANSLATING:
        translate_status.status(msg)
        return
    elif st.session_state.state == core.CurrentState.SUBTITLE_MERGING:
        subtitles_status.status(msg)
        return

def main():
    global split_status, translate_status, subtitles_status

    sys.path.append(os.getcwd() +'/core')
    st.header('字幕 Subtitle')

    model = cfg.get_config_value('gpt.model')
    log_utils.observable_handler.subscribe(update)

    with st.container(border=True):
        st.subheader('✂️ 切分')
        cols = st.columns(3)
        cols[0].text_input('LLM 模型', model)
        cols[1].number_input('max threads', min_value=1, max_value=100, value=3, step=1)
        cols[2].number_input('batch size', min_value=1, max_value=100, value=5, step=1)
        split_status = st.empty()
        if(st.button('LLM 切分')):
            st.session_state.state = core.CurrentState.LLM_SPILITTING
            core.split_main.start_split()
            split_status.status('切分完成', state='complete')

    with st.container(border=True):
        st.subheader('💬 翻译')
        cols = st.columns(3)
        cols[0].text_input('LLM 翻译模型', model)
        cols[0].checkbox('专家模式')
        cols[1].number_input('Max threads', min_value=1, max_value=100, value=3, step=1)
        cols[2].number_input('Batch size', min_value=1, max_value=100, value=5, step=1)
        translate_status = st.empty()
        if(st.button('开始翻译')):
            st.session_state.state = core.CurrentState.TRANSLATING
            update('翻译中...')
            core.gpt_translator.start_translate()
            translate_status.status('翻译完成', state='complete')

    with st.container(border=True):
        st.subheader('📜 时间轴')
        cols = st.columns(2)
        cols[0].color_picker("翻译字幕颜色", "#FFFFFF")
        cols[1].color_picker("字幕颜色", "#FFFFFF")
        subtitles_status = st.empty()
        if(st.button('双语字幕生成')):
            st.session_state.state = core.CurrentState.SUBTITLE_MERGING
            core.sub_timeline_fit.start()
            subtitles_status.status('双语字幕生成完成', state='complete')

main()