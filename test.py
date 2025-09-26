import librosa
import numpy as np
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

def load_audio(file_path):
    """加载音频文件并返回左右声道"""
    # 加载音频文件，保持双声道
    audio, sr = librosa.load(file_path, sr=None, mono=False)
    
    # 如果是单声道，复制为双声道
    if audio.ndim == 1:
        audio = np.array([audio, audio])
    
    # 分离左右声道
    left_channel = audio[0]
    right_channel = audio[1]
    
    return left_channel, right_channel, sr

def extract_features(audio, sr):
    """提取音频特征"""
    # 提取MFCC特征
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    
    # 提取色度特征
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    
    # 提取频谱质心
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    
    # 提取过零率
    zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)
    
    return {
        'mfcc': mfcc, 
        'chroma': chroma,
        'spectral_centroid': spectral_centroid,
        'zero_crossing_rate': zero_crossing_rate
    }

def compare_features(features_left, features_right):
    """比较左右声道的特征相似度"""
    similarity_scores = {}
    
    # 比较MFCC特征的余弦相似度
    mfcc_left = features_left['mfcc'].flatten()
    mfcc_right = features_right['mfcc'].flatten()
    min_length = min(len(mfcc_left), len(mfcc_right))
    mfcc_left = mfcc_left[:min_length]
    mfcc_right = mfcc_right[:min_length]
    
    similarity_scores['mfcc_cosine'] = 1 - spatial.distance.cosine(mfcc_left, mfcc_right)
    
    # 比较其他特征的相似度
    for feature_name in ['chroma', 'spectral_centroid', 'zero_crossing_rate']:
        feat_left = features_left[feature_name].flatten()
        feat_right = features_right[feature_name].flatten()
        min_length = min(len(feat_left), len(feat_right))
        feat_left = feat_left[:min_length]
        feat_right = feat_right[:min_length]
        
        # 计算相关系数
        correlation = np.corrcoef(feat_left, feat_right)[0, 1]
        similarity_scores[f'{feature_name}_correlation'] = correlation
    
    return similarity_scores

def detect_vocal_differences(file_path, threshold=0.8):
    """检测双声道中人声差异"""
    # 加载音频
    left_channel, right_channel, sr = load_audio(file_path)
    
    # 提取特征
    features_left = extract_features(left_channel, sr)
    features_right = extract_features(right_channel, sr)
    
    # 比较特征
    similarity_scores = compare_features(features_left, features_right)
    
    # 计算总体相似度（取各特征相似度的平均值）
    overall_similarity = np.mean(list(similarity_scores.values()))
    
    # 判断人声是否不同
    is_different = overall_similarity < threshold
    
    return {
        'is_different': is_different,
        'overall_similarity': overall_similarity,
        'similarity_scores': similarity_scores,
        'left_channel': left_channel,
        'right_channel': right_channel,
        'sample_rate': sr
    }

def visualize_comparison(result, output_path=None):
    """可视化比较结果"""
    left = result['left_channel']
    right = result['right_channel']
    sr = result['sample_rate']
    
    # 创建时间轴
    time = np.arange(0, len(left)) / sr
    
    plt.figure(figsize=(12, 10))
    
    # 绘制波形图
    plt.subplot(3, 1, 1)
    plt.plot(time, left, alpha=0.7, label='Left Channel')
    plt.plot(time, right, alpha=0.7, label='Right Channel')
    plt.title('Waveform Comparison')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    # 绘制频谱图
    plt.subplot(3, 1, 2)
    D_left = librosa.amplitude_to_db(np.abs(librosa.stft(left)), ref=np.max)
    D_right = librosa.amplitude_to_db(np.abs(librosa.stft(right)), ref=np.max)
    
    librosa.display.specshow(D_left, sr=sr, x_axis='time', y_axis='log', alpha=0.5, cmap='Reds')
    librosa.display.specshow(D_right, sr=sr, x_axis='time', y_axis='log', alpha=0.5, cmap='Blues')
    plt.title('Spectrogram Comparison (Red: Left, Blue: Right)')
    plt.colorbar(format='%+2.0f dB')
    
    # 绘制相似度分数
    plt.subplot(3, 1, 3)
    features = list(result['similarity_scores'].keys())
    scores = list(result['similarity_scores'].values())
    
    colors = ['green' if score > 0.8 else 'orange' if score > 0.6 else 'red' for score in scores]
    bars = plt.bar(features, scores, color=colors)
    plt.axhline(y=0.8, color='r', linestyle='--', alpha=0.7, label='Threshold (0.8)')
    plt.title('Feature Similarity Scores')
    plt.ylabel('Similarity Score')
    plt.xticks(rotation=45)
    plt.legend()
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    
    plt.show()

# 使用示例
if __name__ == "__main__":
    # 替换为你的音频文件路径
    audio_file = "C:\\Users\lingc\\Music\\this body means nothing to me.mp3"
    
    # 检测人声差异
    result = detect_vocal_differences(audio_file)
    
    # 打印结果
    print(f"总体相似度: {result['overall_similarity']:.4f}")
    print(f"人声是否不同: {result['is_different']}")
    
    print("\n各特征相似度:")
    for feature, score in result['similarity_scores'].items():
        print(f"{feature}: {score:.4f}")
    
    # 可视化比较结果
    visualize_comparison(result)