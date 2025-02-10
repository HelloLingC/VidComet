import streamlit as st
from helper import ytp
import helper.ytp

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
    # cst.change(language='cn')
    # st.sidebar.header('Left')
    # st.image('icon.png')
    st.markdown(css, unsafe_allow_html=True)
    st.title('SubtitleComet')
    input_mode = st.selectbox('选择视频输入源：', options_input_mode)
    if input_mode == options_input_mode[0]:
        uploaded_file = st.file_uploader("选择视频", type=["mp4", "avi", "mov", "mkv"])
    else:
        col1, col2 = st.columns(2)
        url_input = st.text_input('输入视频URL')
        res = col1.selectbox('视频分辨率', options_download_res)
        col2.text_input('Cookies')
    if(st.button('开始')):
        if input_mode == options_input_mode[0]:
            if uploaded_file is None:
                st.error("请上传视频文件！")
                return
            # start_via_file(uploaded_file)
            st.spinner('正在处理...')
            st.switch_page('pages')
        else:
            st.spinner('正在下载...')
            start_via_url(url_input, res)
            
main()