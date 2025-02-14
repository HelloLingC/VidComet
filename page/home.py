import streamlit as st
from core import ytp
import tkinter as tk
from tkinter import filedialog

options_input_mode = ['本地文件', '远程文件流']
options_download_res = ['最高画质', '1080p', '720p', '480p', '360p']

def start_via_file(file):
    if(file is None):
        
        return

def start_via_url(url, res):
    if(url == ""):
        st.error("请输入视频URL！")
        return
    ytp.download(url, res=res)

css = '''
<style>
#subtitlecomet {
    background: linear-gradient(90deg, #ff7e5f, #feb47b); 
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
</style>
'''

def main():
    # if 'vid_file' not in st.session_state:
    #     st.session_state.vid_file = None
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()
    
    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # cst.change(language='cn')
    # st.sidebar.header('Left')
    # st.image('icon.png')
    st.markdown(css, unsafe_allow_html=True)
    st.title('SubtitleComet')
    input_mode = st.selectbox('选择视频输入源：', options_input_mode)
    if input_mode == options_input_mode[0]:
        uploaded_file = st.file_uploader("上传视频", type=["mp4", "avi", "mov", "mkv"])
        if st.button('选择本地视频'):
            fname = str(filedialog.askopenfilename(master=root))
            # st按钮点击后，会重新更新界面，导致fname值被flush
            # 包括打开tk的文件选择窗口之后
            if fname:
                st.session_state.vid_file = fname
                st.text_input('选择的文件：', fname)
    else:
        col1, col2 = st.columns(2)
        url_input = st.text_input('输入视频URL')
        res = col1.selectbox('视频分辨率', options_download_res)
        col2.text_input('Cookies')
    if(st.button('下一步', icon='🚀')):
        fname = st.session_state.vid_file
        if uploaded_file is None and fname is None:
                st.error("请上传视频文件！")
                return
        if input_mode == options_input_mode[0]:
            # start_via_file(uploaded_file)
            st.spinner('正在处理...')
            st.session_state.file_path = fname
            st.switch_page('page/preprocess.py')
        else:
            st.spinner('正在下载...')
            start_via_url(url_input, res)
    # 提前的导入下一页面的whisperx包，防止下一页空白期过久
    # (足足有7秒)
    __import__('whisperx')
 
main()