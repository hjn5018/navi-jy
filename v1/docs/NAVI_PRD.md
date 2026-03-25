# NAVI PRD (v2.0)

## 1. 개요 (Product Overview)
*   **제품명**: NAVI (Navigation & Voice Interface)
*   **핵심가치**: 사용자의 음성 및 텍스트 명령을 실시간으로 분석하여 웹 탐색(YouTube 등)과 Windows OS 제어(메모장 입력 등)를 자동화함.
*   **대상 사용자**: PC 조작을 더욱 간편하게 하고 싶은 일반 사용자 및 반복적인 자동화 작업이 필요한 사용자.

## 2. 핵심 기능 (Key Features)
### 2.1 인텐트 라우팅 (Intent Routing)
*   LLM(GPT-4o-mini)을 이용한 사용자 발화 분석.
*   "Web Search", "OS Control", "General Info"로 의도 자동 분류.

### 2.2 웹 에이전트 (Web Agent)
*   **유튜브 검색**: Playwright를 이용한 정밀 정보 파싱 (제목, 조회수, 재생 시간, 링크).
*   **브라우저 자동화**: 검색 결과 자동 브라우징 및 상호작용.

### 2.3 OS 제어 에이전트 (OS Control Agent)
*   Windows `uiautomation`을 이용한 데스크톱 앱 제어.
*   메모장 열기, 텍스트 입력, 저장 등의 작업 수행.

### 2.4 실시간 실물 대시보드 (Real-time Dashboard)
*   Next.js 16 기반 고정밀 모던 UI.
*   **Compact 모드**: 플로팅 오버레이 상태로 최소화된 위젯 사용 가능.
*   **WebSocket**: 백엔드와의 실시간 상태 동기화 및 라이브 로그 표시.

## 3. 기술 스택 (Technical Stack)
*   **Frontend**: Next.js 16, Tailwind CSS v4, Lucide-React
*   **Backend**: FastAPI, WebSocket
*   **Agent**: Playwright (Web), uiautomation (Windows), LangChain + OpenAI (LLM)
*   **Security**: Data Masking (이메일/비번 자동 필터링)

## 4. UI/UX 컨셉
*   **Light Mode**: 화이트/블루 계열의 깨끗하고 정교한 디자인.
*   **Accessibility**: 큰 입력창과 직관적인 상태 아이콘(MIC, ROUTER)으로 정보 가독성 극대화.
