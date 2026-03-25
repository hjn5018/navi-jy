# NAVI V2 개발 태스크 리스트 (To-Do List)

## Phase 1: 기반 설정 및 로컬 AI 연동 (Infrastructure & Local AI)
- [ ] V2 프론트엔드/데스크톱 셸 보일러플레이트 생성 (Tauri + React/Vite)
- [ ] V2 파이썬 엔진 보일러플레이트 생성 (Python Sidecar) 및 환경 분리
- [ ] Faster-Whisper 로컬 연동 테스트 (마이크 -> 텍스트 변환 딜레이 최적화)
- [ ] Piper TTS / Silero TTS 로컬 연동 테스트

## Phase 2: 코어 에이전트 및 LLM 연동 (Agent & Function Calling)
- [ ] Ollama 설치 및 추론 모델(Phi-3 또는 Qwen2) 로컬 세팅
- [ ] LLM Prompt Engineering: STT 오타 교정 및 인텐트 파악 프롬프트 작성
- [ ] LLM Function Calling (Tool Calling) 인터페이스 구현
- [ ] Tool Dispatcher 서브시스템 구축 (LLM JSON 출력 파싱 기능)

## Phase 3: 액션 워커 개발 (OS & Web Automation workers)
- [ ] Windows OS 제어 워커 리팩토링 및 이식 (uiautomation/pyautogui 활용)
- [ ] Playwright 기반 웹 브라우저 자동화 워커 기능 구현
- [ ] 각 워커들을 Tool Dispatcher에 매핑 (등록)

## Phase 4: 통합 및 UI 연동 (Integration & UI)
- [ ] Tauri IPC (Inter-Process Communication) 파이프라인 완성 (React <-> Python)
- [ ] 프론트엔드 UI/UX 작업 (마이크 스피치 웨이브폼 애니메이션 등)
- [ ] 통합 테스트 (음성 명령 -> LLM 교정 -> OS 제어 -> TTS 응답)
- [ ] Tauri Build / 앱 패키징 데스크톱 설치 파일(.msi / .exe) 배포 설정

## Phase 5: 안정화 및 QA (Polishing & QA)
- [ ] 복합 명령 처리(예: 브라우저 열고 검색 후 결과 읽기) 테스트
- [ ] 로컬 환경 속도 최적화 (모델 양자화 적용 등)
- [ ] 최종 사용자 가이드라인 문서 및 README.md 업데이트
