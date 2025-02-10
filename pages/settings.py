import streamlit as st
import torch

col1, col2 = st.columns(2)
with col1.expander('LLM 设置', True):
    st.text_input('API Key')

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