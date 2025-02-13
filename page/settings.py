import streamlit as st
import torch
from core import env_check

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

col0, col1, col2 = st.columns(3)

with col0.expander('Nvidia 信息', True):
    st.text("Torch 版本：" + torch.__version__)
    st.text("CUDA 版本：" + torch.version.cuda)
    st.text("cuDNN 版本：" + str(torch.backends.cudnn.version()))
    if torch.cuda.is_available():
        st.success('当前GPU可用')
        st.info("CUDA 设备：" + torch.cuda.get_device_name(torch.cuda.current_device()))
    else:
        st.error('当前GPU不可用')

with col1.expander('LLM 设置', True):
    st.text_input('API Url')
    st.text_input('API Key')
    st.text_input('模型', 'deepseek-r1')

with col1.expander('FFmpeg', True):
    ver = env_check.check_ffmpeg()
    # Todo
    if ver != None:
        st.text('版本：' + str(ver))

with col1.expander('Demucs 设置', True):
    # Pre-trained model
    st.selectbox('模型', ['htdemucs', 'htdemucs-ft', 'htdemucs_6s', 'mdx_extra_q'])

with col2.expander('WhisperX 设置', True):
    st.selectbox('目标语言', ['auto', 'zh', 'en', 'jp'])
    st.selectbox('模型', ['Whisper-large-v3-turbo', 'Whisper-large-v3', 'Belle-whisper-large-v3-zh', 'Huan69/Belle-whisper-large-v3-zh-punct-fasterwhisper'])
    st.selectbox('计算设备', ['GPU', 'CPU'])
    st.checkbox('计算类型 float16', True)
    st.write('如果显存低请取消勾选')
    st.number_input('Batch Size')
    env_check.check_ffmpeg()