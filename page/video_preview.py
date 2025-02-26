import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import os
import json
import utils.config_utils as cfg
import utils.srt_parser
import pandas as pd
from string import Template

def ai_summary(summary: str):
    # Todo: Dark theme
    css = """
 <style>
        .summary_container {
            border: 1px solid rgba(49, 51, 63, 0.2);
            box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;s
            border-radius: 0.5rem;
            padding: 1rem;
            max-width: 760px;
        }
        .summary_container span {
            font-size: 1.2rem;
            font-weight: 600;
            color: #fbdb3c;
        }
    </style>
    """

    html="""
        <div class="summary_container">
        <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fbdb3c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
        由 AI 生成的摘要
        </span>
        <p>${summary}</p>
        </div>
        """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(Template(html.strip()).substitute(summary=summary), unsafe_allow_html=True)

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
    col1, col2 = st.columns([1, 1])
    with col1.container():
        assert os.path.exists(cfg.SRT_PATH)
        ori, trans = utils.srt_parser.parse_trans_and_ori_srt()
        df = pd.DataFrame(ori)
        df = df.rename(columns={'start_time': '开始', 'text': '原文'})
        df['翻译'] = trans
        # df['active'] = False
        st.data_editor(df,
                #      column_config={
                #     "active": st.column_config.CheckboxColumn(
                #         "Your favorite?",
                #         help="Select your **favorite** widgets",
                #         default=False,
                #     )
                # },
    hide_index=False,
    num_rows='fixed',
    )

    if os.path.exists(cfg.OUTPUT_VIDEO):
        col2.video(cfg.OUTPUT_VIDEO)
    else:
        st.error('视频文件不存在')

    if(os.path.exists(cfg.SUMMARY_PATH)):
        with open(cfg.SUMMARY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            summary = data['summary'].replace('.', '.\n\n').strip()
            terms = data['terms']

        ai_summary(summary)
        with st.chat_message('ai'):

            term_text = ""
            for term in terms:
               term_text += f"""
- {term['src']} - {term["tgt"]}
    - {term['note']}"""
            st.markdown(f'##### 术语表\n{term_text}')
    else:
        st.warning('摘要文件不存在')

main()