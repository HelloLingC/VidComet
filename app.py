import streamlit as st
from helper import ytp
import helper.ytp
import torch
import os
from streamlit_change_language import cst
import sys
import os

# to keep away
# RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

st.set_page_config(page_title='Subtitle Comet', page_icon='icon.png')

def main():
    sys.path.append(os.getcwd() + '/helper')
    # print(sys.path)
    print(os.path.abspath(__file__))
    # cst.change(language='cn')
    st.logo('icon.png')
    st.sidebar.header('导航栏')
    
    p1 = st.Page('page/home.py', title='开始')
    
    p2 = st.Page('page/subtitle.py', title='字幕翻译')
    p3 = st.Page('page/subtitle.py', title='视频剪辑')
    settings = st.Page('page/settings.py', title='设置')
    pg = st.navigation([p1, p2, settings])
    pg.run()

if __name__ == '__main__':
    main()