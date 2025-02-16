import streamlit as st
import os
import json
import core.config_utils as cfg

def main():
    st.header('Video Preview')
    if os.path.exists(cfg.OUTPUT_VIDEO):
        st.video(cfg.OUTPUT_VIDEO)
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
- {term['src']}
    - {term["tgt"]}
    - {term['note']}"""
            st.markdown(f'##### 术语表\n{term_text}')
    else:
        st.warning('摘要文件不存在')

main()