import torch
import sounddevice as sd
import time

print("Silero TTS 모델 로딩 중... (최초 실행 시 모델 다운로드가 진행될 수 있습니다)")
start_time = time.time()

language = 'en'
model_id = 'v3_en'
device = torch.device('cpu')

# Silero TTS 로드
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)

model.to(device)  # CPU로 이동
print(f"모델 로드 완료: {time.time() - start_time:.2f}초")

test_text = "Welcome to Navi V2. The local text to speech system is working perfectly."
sample_rate = 48000
speaker = 'en_0'

print(f"\n텍스트 변환 시도: '{test_text}'")
start_time = time.time()
audio = model.apply_tts(text=test_text,
                        speaker=speaker,
                        sample_rate=sample_rate)

print(f"음성 합성 완료: {time.time() - start_time:.2f}초")

print("음성 재생 중...")
sd.play(audio.numpy(), samplerate=sample_rate)
sd.wait()
print("재생 완료.")
