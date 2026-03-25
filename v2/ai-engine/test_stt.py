import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import time
import os

fs = 16000  # Sample rate
seconds = 3  # Duration of recording
filename = "test_audio.wav"

print(f"[{seconds}초 동안 마이크로 음성을 녹음합니다. 말씀해주세요...]")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # Wait until recording is finished
write(filename, fs, myrecording)  # Save as WAV file 
print("[녹음 완료]")

model_size = "tiny"
print(f"\n{model_size} 모델을 로드하는 중... (CPU 모드)")
start_time = time.time()
# CPU 모드로 int8 양자화 적용 (가장 가벼운 설정)
model = WhisperModel(model_size, device="cpu", compute_type="int8")
print(f"모델 로드 완료: {time.time() - start_time:.2f}초")

print("\n음성 인식(STT) 진행 중...")
start_time = time.time()
segments, info = model.transcribe(filename, beam_size=5)

print(f"감지된 언어: '{info.language}' (확률: {info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
print(f"추론 소요 시간: {time.time() - start_time:.2f}초")

# 테스트 완료 후 파일 삭제
if os.path.exists(filename):
    os.remove(filename)
