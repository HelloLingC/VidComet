import streamlit as st
import torch
from helper import env_check

col1, col2 = st.columns(2)
with col1.expander('LLM 设置', True):
    st.text_input('API Key')

with col1.expander('FFmpeg', True):
    ver = env_check.check_ffmpeg()
    # Todo
    if ver != None:
        st.text('版本：' + str(ver))

with col1.expander('Demucs 设置', True):
    # Pre-trained model
    st.selectbox('预训练模型', ['htdemucs', 'htdemucs-ft', 'htdemucs_6s', 'mdx_extra_q'])

with col2.expander('WhisperX 设置', True):
    st.selectbox('模型', ['large-v2', 'small'])
    st.selectbox('计算设备', ['GPU', 'CPU'])
    if not torch.cuda.is_available():
        st.warning('当前GPU不可用')
    else:
        st.success('当前GPU可用')
    st.checkbox('计算类型 float16', True)
    st.write('如果显存低请取消勾选')
    st.number_input('Batch Size')
    env_check.check_ffmpeg()