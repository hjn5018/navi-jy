# 🛠️ NAVI 기술 스택 및 개발 여정 (Tech Deep Dive)

NAVI 프로젝트는 최신 웹 기술과 강력한 AI 생태계를 결합하여, 사용자 친화적인 보이스 어시스턴트를 구축하는 것을 목표로 했습니다.

## 1. 왜 이 기술들을 선택했나요? (Core Tech Choices)

### ⚛️ Frontend: Next.js (React Framework)
*   **선택 이유**: modern UI를 가장 빠르고 완성도 있게 구현할 수 있는 도구이며, Tailwind CSS와의 최적화가 우수합니다.
*   **결정적 역할 (Static Export)**: `output: 'export'`를 통해 빌드된 결과물을 백엔드가 직접 서빙하게 함으로써 단일 EXE 배포를 가능하게 했습니다.
*   **기술적 대안 (SSG/Vite)**: 본 프로젝트의 방식은 Next.js에 국한되지 않습니다. `Vite(React/Vue)`, `Nuxt`, `SvelteKit` 등 정적 사이트 생성(SSG)을 지원하는 어떠한 현대적 프레임워크로도 동일한 아키텍처 구현이 가능합니다.

### ⚡ Backend: FastAPI (Python Framework)
*   **선택 이유**: Python의 강력한 AI 생태계를 활용하면서도, 높은 비동기 성능을 제공합니다.
*   **비동기 처리의 실익**: WebSocket 관리, LLM API 대기, 웹 스크래핑 시 I/O 차단을 방지하여 실시간성을 유지합니다.
*   **타 기술과의 비교 (Asynchronous Alternatives)**:
    - **Node.js**: 단일 스레드 이벤트 루프 방식으로 비동기 처리에 매우 강력하지만, CPU 부하가 큰 AI 연산 시 Python 대비 라이브러리 지원이 다소 제한적일 수 있습니다.
    - **Go (Goroutines)**: 경량화된 고루틴을 통해 수만 개의 동시성 처리가 가능하며 속도가 매우 빠르지만, AI 개발 생산성 측면에서 Python이 우위에 있습니다.
    - **Elixir (Erlang VM)**: 고도의 가용성과 액터 모델 기반 비동기 처리를 제공하지만, 학습 곡선이 높습니다.
    NAVI는 **AI 개발 생산성**과 **비동기 성능**의 균형을 위해 FastAPI를 최적으로 선택했습니다.

### 🎙️ Voice & Audio Strategy
*   **STT (Speech-to-Text)**:
    - **Local Choice (Web Speech API)**: 브라우저 내장 엔진을 사용하여 서버 부하와 패키징 용량을 최소화했습니다. 별도 설치 없이 100% 무료로 작동합니다.
    - **Cloud Choice (OpenAI Whisper)**: 고정밀 변환이 필요한 경우 선택적으로 API를 통해 처리합니다.
*   **TTS (Text-to-Speech)**:
    - **Edge-TTS**: Microsoft의 무료 신경망 음성 엔진을 사용하여 API 키 없이도 로컬에서 고품질 음성을 생성합니다.

---

## 2. 주요 패키지 및 역할 (Core Packages)

| 패키지 | 역할 | 비고 |
| :--- | :--- | :--- |
| **LangChain** | LLM 오케스트레이션 | GPT-4o-mini 연동 및 의도(Intent) 분석 |
| **Playwright** | 웹 브라우저 자동화 | YouTube 검색 및 구조적 데이터 추출 |
| **uiautomation** | **OS 제어 및 자동화** | **메모장(텍스트 입력), 계산기(수식 연산), 일반 전용 앱(그림판 등) 제어 매크로 구현** |
| **pywebview** | 네이티브 GUI 윈도우 | 웹 대시보드를 윈도우 앱 창으로 변환 |
| **PyInstaller** | 통합 EXE 패키징 | 모든 소스와 의존성을 하나로 응축 |
| **Uvicorn** | ASGI 서버 | 고성능 비동기 통신 및 웹소켓 엔진 |
| **Websockets** | 실시간 양방향 통신 | 에이전트 상태 및 결과 실시간 전송 |

---

## 3. OS 지능형 제어 (Refactored OS Agent)
기존의 단순 POC 수준을 넘어, 프로젝트 구조를 리팩토링하여 `OSAgent` 클래스로 통합 관리하고 있습니다.
*   **시나리오 기반 제어**: "메모장에 적어줘", "계산기에서 풀어줘"와 같은 명령에 따라 윈도우 객체를 찾아 정밀 제어합니다.
*   **브라우저 연동**: 지도 검색이나 단순 웹 검색 시, 파이썬 기반 에이전트가 직접 브라우저를 컨트롤하여 특정 URL로 즉시 이동시킵니다.

---

## 3. 개발 및 빌드 주요 명령어 (Major Commands)

### 🏗️ 개발 단계
*   `npm run dev`: 프론트엔드 실시간 개발 서버 구동
*   `python -m uvicorn backend.main:app --reload`: 백엔드 API & 에이전트 서버 구동

### 🚀 빌드 및 패키징 단계
1.  **프론트엔드 정적 파일 생성**:
    ```bash
    cd client && npm run build
    ```
    (결과물: `client/out` 폴더 생성)

2.  **All-in-One 실행 파일 빌드**:
    ```bash
    python -m PyInstaller --onefile --noconsole --name NAVI_App \
      --add-data "client/out;client/out" \
      --add-data "backend;backend" \
      --collect-all langchain \
      --collect-all uvicorn \
      --collect-all websockets \
      --collect-all webview \
      launcher.py
    ```

---

## 🏁 요약: 아키텍처의 의의
NAVI는 **"Python의 AI 처리 능력"**과 **"React의 세련된 UI"**를 결합하되, 배포 시에는 사용자가 복잡한 설치 과정 없이 **`.exe` 하나만 실행**하면 되도록 설계되었습니다. 이는 개발 편의성과 사용자 경험(UX)이라는 두 마리 토끼를 잡기 위한 전략적 선택이었습니다.
