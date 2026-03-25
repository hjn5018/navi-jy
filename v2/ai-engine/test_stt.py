import sounddevice as sd
from scipy.io.wavfile import write
import time
import os

# HuggingFace symlink warning 제거
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import numpy as np
import whisper

fs = 16000  # Sample rate
seconds = 10  # Duration of recording

print(f"[{seconds}초 동안 마이크로 음성을 녹음합니다. 말씀해주세요...]")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
print("[녹음 완료]")

# CPU 환경 충돌 및 Segmentation fault 방지
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

model_size = "tiny"
print(f"\n{model_size} 모델을 로드하는 중... (CPU 모드)")
start_time = time.time()
model = whisper.load_model(model_size, device="cpu")
print(f"모델 로드 완료: {time.time() - start_time:.2f}초")

print("\n음성 인식(STT) 진행 중...")
start_time = time.time()

# ffmpeg 설치 요구를 피하기 위해 numpy 배열을 float32로 정규화 후 직접 전달
audio_data = myrecording.flatten().astype(np.float32) / 32768.0
result = model.transcribe(audio_data)

print(f"인식 결과:")
print(f"[0.00s -> {seconds:.2f}s] {result['text']}")
print(f"추론 소요 시간: {time.time() - start_time:.2f}초")
