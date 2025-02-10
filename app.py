import streamlit as st
from helper import ytp
import helper.ytp
from streamlit_change_language import cst

st.set_page_config(page_title='Subtitle Comet', page_icon='icon.png')

def main():
    # cst.change(language='cn')
    st.logo('icon.png')
    st.sidebar.header('导航栏')
    
    p1 = st.Page('pages/home.py', title='开始')
   
    p2 = st.Page('pages/subtitle.py', title='字幕翻译')
    p3 = st.Page('pages/subtitle.py', title='视频剪辑')
    settings = st.Page('pages/settings.py', title='设置')
    pg = st.navigation([p1, p2, settings])
    pg.run()

if __name__ == '__main__':
    main()