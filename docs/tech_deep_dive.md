# 🛠️ NAVI 기술 스택 및 개발 여정 (Tech Deep Dive)

NAVI 프로젝트는 최신 웹 기술과 강력한 AI 생태계를 결합하여, 사용자 친화적인 보이스 어시스턴트를 구축하는 것을 목표로 했습니다.

## 1. 왜 이 기술들을 선택했나요? (Core Tech Choices)

### ⚛️ Frontend: Next.js (React Framework)
*   **선택 이유**: modern UI를 가장 빠르고 완성도 있게 구현할 수 있는 도구입니다. 특히 Tailwind CSS와의 궁합이 좋아 고퀄리티의 디자인을 신속하게 확보할 수 있었습니다.
*   **결정적 역할 (Static Export)**: `output: 'export'` 기능을 통해 모든 화면을 정적 HTML/JS 파일로 뽑아낼 수 있습니다. 이는 서버 없이도 백엔드에서 직접 화면을 서빙(Serving)하게 함으로써, **단일 실행 파일(.exe)** 제작을 가능하게 만든 핵심 요소입니다.
*   **역할**: UI/UX 제공, 실시간 음성/텍스트 입력 처리, WebSocket 통신 클라이언트.

### ⚡ Backend: FastAPI (Python Framework)
*   **선택 이유**: Python은 LLM(LangChain)과 AI 생태계의 중심입니다. FastAPI는 그중에서도 가장 빠르고(Asynchronous), WebSocket 처리가 우수하며 코드 작성이 직관적입니다.
*   **결정적 역할 (Async & Socket)**: AI 에이전트의 복합적인 작업(웹 검색, LLM 추론)을 비동기적으로 처리하여 사용자에게 끊김 없는 경험을 제공합니다.
*   **역할**: 메인 에이전트 로직(Agent Manager), LangChain을 활용한 의도 분석, 실시간 WebSocket 서버(Uvicorn), 정적 UI 파일 서빙.

---

## 2. 주요 패키지 및 역할 (Core Packages)

| 패키지 | 역할 | 비고 |
| :--- | :--- | :--- |
| **LangChain** | LLM 오케스트레이션 | GPT-4o-mini 연동 및 의도(Intent) 분석 |
| **Playwright** | 웹 브라우저 자동화 | YouTube 검색 및 구조적 데이터 추출 |
| **pywebview** | 네이티브 GUI 윈도우 | 웹 대시보드를 윈도우 앱 창으로 변환 |
| **PyInstaller** | 통합 EXE 패키징 | 모든 소스와 의존성을 하나로 응축 |
| **Uvicorn** | ASGI 서버 | 고성능 비동기 통신 및 웹소켓 엔진 |
| **Websockets** | 실시간 양방향 통신 | 에이전트 상태 및 결과 실시간 전송 |

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
