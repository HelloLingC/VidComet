import streamlit as st
import core.ytp
from core import config_utils
import torch
import os
# from streamlit_fillter import cst
import sys
import os

# to keep away
# RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 

st.set_page_config(page_title='Subtitle Comet', page_icon='icon.png')

def main():
    if(os.getcwd() +'/core' not in sys.path):
        sys.path.append(os.getcwd() +'/core')
    # file_dir = os.path.dirname(__file__)
    # if file_dir not in sys.path:
    #     sys.path.append(file_dir)
    # cst.change(language='cn')
    # config_utils.init_config_helper()
    
    st.logo('icon.png')
    st.sidebar.header('导航栏')
    
    p1 = st.Page('page/home.py', title='开始')
    p2 = st.Page('page/preprocess.py', title='预处理')
    p3 = st.Page('page/transcribe.py', title='转录')
    settings = st.Page('page/settings.py', title='设置')
    pg = st.navigation([p1, p2, p3, settings])
    pg.run()

if __name__ == '__main__':
    main()