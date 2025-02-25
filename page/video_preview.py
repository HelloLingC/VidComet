import streamlit as st
import os
import json
import utils.config_utils as cfg

def main():
    st.markdown(
    """
    <style>
    .stMain {
        align-items: center;
    }
    .stMainBlockContainer {
        max-width: 100%;
        padding: 6rem 3rem 10rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    st.header('Video Preview')
    col1, col2 = st.columns([1, 2])
    with col1.container():
        st.dataframe()

    if os.path.exists(cfg.OUTPUT_VIDEO):
        col2.video(cfg.OUTPUT_VIDEO)
    else:
        st.error('视频文件不存在')

    if(os.path.exists(cfg.SUMMARY_PATH)):
        with open(cfg.SUMMARY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            summary = data['summary'].replace('.', '.\n\n').strip()
            terms = data['terms']
        with st.chat_message('ai'):
            st.markdown(f'##### 由AI生成的摘要\n')
            st.text(summary)
            term_text = ""
            for term in terms:
               term_text += f"""
- {term['src']} - {term["tgt"]}
    - {term['note']}"""
            st.markdown(f'##### 术语表\n{term_text}')
    else:
        st.warning('摘要文件不存在')

main()