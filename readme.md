# VidComet - AI双语字幕视频自动化生成程序

![screenshot](/screenshots/2025-02-16-173003.png)

## 📖 项目简介

VidComet 是基于AI的自动化双语字幕生成工具，能够自动为视频文件生成高质量的双语字幕。该程序集成了语音识别、字幕智能切分、机器翻译和字幕合成等多个模块，为用户提供一站式的视频字幕制作解决方案。

### ✨ 主要功能

- 🎵 **音频分离**: 使用 Demucs 模型分离视频中的人声和背景音
- 🎧 **语音识别**: 基于 WhisperX 的语音转文字ASR
- ✂️ **智能切分**: 使用大语言模型智能切分字幕段落
- 🌐 **自动翻译**: 支持多种语言翻译，默认中英双语
- 📺 **视频预览**: 实时预览字幕效果
- 🖥️ **Web界面**: 基于 Streamlit 的友好用户界面

### 🔧 技术栈

- **语音识别**: WhisperX (基于 OpenAI Whisper)
- **音频分离**: Demucs
- **大语言模型**: 支持 OpenAI API 和本地 Ollama
- **Web框架**: Streamlit
- **深度学习**: PyTorch
- **字幕格式**: SRT

## 🚀 快速开始

### 系统要求

- **Python**: 3.10 ~ 3.12
- **CUDA**: 12.6 (推荐)
- **CUDNN**: 9.3
- **内存**: 建议 8GB+ RAM
- **存储**: 至少 10GB 可用空间

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/MoonLab-Studio/SubtitleComet.git
cd SubtitleComet
```

2. **安装 PyTorch (GPU版本)**
```bash
pip3 install torch torchaudio --index-url https://download.pytorch.org/whl/cu126
```

3. **安装项目依赖**
```bash
pip3 install -r requirements.txt
```

4. **下载语言模型**
```bash
# 下载 spaCy 语言模型
python -m spacy download en_core_web_md
python -m spacy download zh_core_web_md
```

### 运行程序

**Web界面模式 (推荐)**
```bash
streamlit run app.py
```

**命令行模式**
```bash
python main.py
```

## 📋 使用指南

### Web界面使用

1. **上传视频**: 在首页选择本地视频文件或输入视频URL
2. **预处理**: 系统自动分离音频并进行语音识别
3. **字幕生成**: 使用LLM智能切分和翻译字幕
4. **预览效果**: 在视频预览页面查看最终效果
5. **导出字幕**: 下载生成的SRT字幕文件

### 配置说明

编辑 `config.yaml` 文件来配置：

```yaml
gpt:
  api_url: http://localhost:11434/v1  # LLM API地址
  api_key: ollama                      # API密钥
  model: qwen2.5-coder:7b             # 使用的模型

whisper:
  language: auto                       # 自动检测语言
  model: large-v2                      # Whisper模型大小
  mode: local                          # 本地模式

translator:
  target: Chinese                      # 翻译目标语言
```

## 📁 项目结构

```
VidComet/
├── app.py                 # Streamlit主应用
├── main.py               # 命令行入口
├── config.yaml           # 配置文件
├── requirements.txt      # 依赖列表
├── core/                 # 核心功能模块
│   ├── whisper_local.py  # Whisper语音识别
│   ├── gpt_translator.py # GPT翻译模块
│   ├── demucs_local.py   # 音频分离
│   └── split_main.py     # 字幕切分
├── page/                 # Web页面
│   ├── home.py          # 首页
│   ├── transcribe.py    # 转录页面
│   ├── splitter.py      # 字幕生成页面
│   └── video_preview.py # 视频预览页面
├── utils/                # 工具模块
├── output/               # 输出文件
└── models/               # 模型文件
```

## ⚙️ 高级配置

### 支持的LLM服务

- **OpenAI API**: 使用官方GPT模型
- **本地Ollama**: 支持本地部署的开源模型
- **DeepSeek API**: 支持DeepSeek模型

### 音频处理选项

- **模型选择**: htdemucs, htdemucs-ft, htdemucs_6s, mdx_extra_q
- **GPU加速**: 自动检测CUDA可用性
- **批处理**: 支持批量处理多个音频文件

### 字幕优化

- **智能切分**: 基于语义的段落切分
- **时间轴对齐**: 精确的字幕时间同步
- **多语言支持**: 支持中、英、日、韩等多种语言

## 📊 输出文件说明

程序会在 `output/` 目录下生成以下文件：

- `srt.srt`: 原始语言字幕文件
- `srt_translation.srt`: 翻译后字幕文件
- `transcript.csv`: 详细转录数据
- `summary.json`: 处理摘要信息
- `audio/`: 音频处理中间文件

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目的支持：

- [WhisperX](https://github.com/m-bain/whisperX) - 高精度语音识别
- [Demucs](https://github.com/adefossez/demucs) - 音频源分离
- [Streamlit](https://streamlit.io/) - Web应用框架
- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别基础模型

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！

