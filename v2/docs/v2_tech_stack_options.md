# NAVI V2 기술 스택 후보군 및 추천 (Tech Stack Options)

V1의 한계(API 비용 발생, 음성 인식 품질 저하, 액션 실행 오류)를 극복하기 위해, **완전 로컬 구동** 및 **정확한 의도 파악과 함수 실행**에 초점을 맞춘 3가지 기술 스택 조합을 제안합니다.

---

## 💡 후보 1: 무거운/고성능 로컬 AI 조합 (GPU 권장)
가장 정확한 성능을 내지만, 사용자의 PC 사양(특히 VRAM 8GB 이상 GPU)을 크게 요구하는 구성입니다.

- **STT**: `faster-whisper` (large-v3 모델) - 현존 최고 수준의 정확도.
- **TTS**: `XTTSv2` (Coqui) 또는 `Bark` - 매우 자연스럽고 감정이 풍부한 음성.
- **LLM**: `Ollama` + `Llama-3 8B Instruct` 또는 `Qwen2 7B` - 강력한 추론 및 Tool Calling 능력.
- **Agent Framework**: `LangGraph` 또는 `LlamaIndex` 기반의 자율 에이전트.
- **Browser/OS Control**: `Playwright` + `pyautogui` / `uiautomation`.

## 💡 후보 2: 경량화/실용성 최적화 조합 (CPU 및 저사양 GPU 호환) ⭐ 추천 ⭐
대다수의 데스크톱 환경에서 부담 없이 실행 가능하면서도, STT 인식 오류를 LLM이 보정하여 액션을 실행할 수 있는 최적의 밸런스 조합입니다.

- **STT**: `faster-whisper` (tiny 또는 base 모델) - 매우 빠르며 메모리 소비가 적음.
- **TTS**: `Piper TTS` 또는 `Silero TTS` - CPU에서도 실시간(수십 ms)으로 텍스트를 음성으로 변환.
- **LLM**: `Ollama` + `Phi-3 mini (3.8B)` 또는 `Qwen2 (1.5B/3B)` - 메모리를 적게 차지하면서도 명시적인 Function Calling / JSON 출력이 훌륭한 모델.
- **Agent Framework**: `Semantic Router` + `Custom Tool Dispatcher` (단순하고 빠르며 LLM의 Function calling API를 직접 호출하여 확실하게 액션 수행).
- **Browser/OS Control**: `Playwright` + `uiautomation`.

## 💡 후보 3: 하이브리드 조합 (빠른 속도, 부분적 네트워크 사용)
오프라인을 완벽히 고집하지 않는 경우, API Key 없이 무료로 사용할 수 있는 클라우드 자원을 일부 섞어 성능을 높이는 조합입니다.

- **STT**: `faster-whisper` (small 모델).
- **TTS**: `Edge-TTS` (마이크로소프트의 Edge 브라우저 TTS API 기반. 무료, 빠름, 고품질. 단, 인터넷 필요).
- **LLM**: `LM Studio` / `Ollama` (Llama-3 8B).
- **Agent Framework**: `LangChain` Agent.
- **Browser/OS Control**: `Playwright` + `uiautomation`.

---

## 🏆 최종 추천 스택 선정: [후보 2] 경량화/실용성 최적화 조합

### 선정 이유 (설루션):
1. **API 비용 제로 및 로컬 구동**: 모든 구성 요소를 로컬에서 실행하므로 보안과 비용 문제가 해결됩니다.
2. **음성 인식 성능 및 속도 향상**: `faster-whisper` base 모델은 V1에서 사용한 것보다 훨씬 빠르며 준수한 인식률을 보입니다.
3. **액션 실행 실패 해결 (LLM Function Calling 도입)**:
4. **앱 프레임워크 및 UI 조합 (V1 구조 탈피 및 네이티브 앱화)**:
   NAVI V2는 파이썬(FastAPI) 백엔드에 얽매이지 않고, **진정한 데스크톱 네이티브 앱** 경험을 제공하기 위해 프론트엔드 셸(Shell)과 AI 파이썬 엔진(Sidecar)을 분리하는 투트랙 아키텍처를 고려합니다. `faster-whisper`나 `uiautomation` 같은 핵심 AI/OS 제어 라이브러리는 파이썬이 필수적이므로 프레임워크들은 파이썬 프로세스를 백그라운드 서버(Sidecar)로 띄우고 통신합니다.

   - **조합 A: Electron + React + Python (Sidecar)**
     - *장점*: 수많은 상용 앱 환경(Discord, VS Code 등)에서 검증된 안정성과 방대한 플러그인 생태계. 웹 기술(Node.js + Chromium)로 데스크톱 앱을 가장 쉽게 제작.
     - *단점*: **매우 높은 메모리(RAM) 점유율**. V2는 로컬 LLM과 로컬 STT를 돌리기 때문에 시스템 자원 확보가 핵심이나 일렉트론 자체만으로 수백 MB의 RAM을 차지합니다.
     
   - **조합 B: Tauri + React/Svelte + Python (Sidecar)** ⭐ *강력 추천*
     - *장점*: Rust 기반으로 내장 WebView를 사용하여 **앱 용량이 매우 작고 메모리 점유율이 일렉트론 대비 압도적으로 낮습니다**. 데스크톱에 설치형 앱을 만들고자 할 때, 무거운 로컬 AI 모델들(Ollama 등)에게 시스템 자원을 양보할 수 있는 최적의 프레임워크입니다. Tauri의 공식 Sidecar 기능으로 파이썬 실행 파일을 쉽게 엮을 수 있습니다.
     - *단점*: Rust 언어 초기 세팅 및 IPC(프로세스 간 통신) 설정이 생소할 수 있습니다.

   - **조합 C: Flutter (Dart) + Python (Local API/gRPC)**
     - *장점*: 웹 뷰(WebView)가 아닌 C++ 엔진 기반 네이티브 캔버스에 직접 렌더링하므로 애니메이션 퍼포먼스와 최적화가 월등합니다(60/120fps 보장).
     - *단점*: 웹 생태계(React/Tailwind) 대신 Dart 언어와 플러터 UI 패키지를 새로 학습해야 합니다. 데스크톱 OS 전용 네이티브 C++ 개발 환경 설정이 요구됩니다.

### 🏆 최종 프레임워크 추천: [조합 B] Tauri + React (Vite) + Python (AI Sidecar)
- V1의 "파이썬으로 웹 서버를 띄워 UI를 제공하던 구조"에서 완전히 벗어나, **Tauri로 네이티브 데스크톱 앱(가벼운 셸)**을 만들고 실제 AI 연산과 윈도우 OS 제어는 백그라운드 **Python 엔진(Sidecar)**이 전담하는 마이크로서비스 형태를 추천합니다.
- 이 구조는 **화려한 최신 웹 기반 UI(React+Tailwind)**를 유지하면서도 **앱 메모리 점유율을 최소화**하여 로컬 AI 구동 환경을 위한 리소스를 최대로 확보할 수 있습니다.

