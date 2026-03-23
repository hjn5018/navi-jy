# NAVI Project To-Do List

## Phase 1: Planning & Architecture
- [x] PRD 고도화 (v2.0)
- [x] 시나리오별 흐름(Use Case, Activity Diagram) 정의
- [x] UI/UX 와이어프레임 설계
- [x] 기술 스택 및 아키텍처 제안
- [x] 핵심 DB 스키마(ERD) 정의

## Phase 2: Environment Setup & PoC (Proof of Concept)
- [ ] Python 백엔드(FastAPI) 프로젝트 초기화 및 가상환경 세팅
- [ ] 프론트엔드/클라이언트 프로젝트 초기화 구축 (Flutter 또는 대안 기술 테스트)
- [ ] OpenAI STT 연동 및 마이크 입력 테스트 스크립트 작성
- [ ] GCP TTS 연동 및 스피커 출력 테스트
- [ ] Playwright를 이용한 유튜브 자동 검색 파이썬 스크립트(PoC) 작성

## Phase 3: Core AI Agent Implementation
- [ ] LangChain/기본 프롬프트를 이용한 의도 분석 인텐트 라우터 개발
- [ ] 웹 브라우저 탐색 에이전트 구현 (DOM 파싱 및 결과 추출)
- [ ] Windows OS 제어 에이전트 구현 (pywinauto / uiautomation 적용)
- [ ] 전체 파이프라인 연동: 음성 입력 -> STT -> 의도 분석 -> Agent 실행 -> 응답 문자열 완성 -> TTS 스피커 출력

## Phase 4: UI Development & Integration
- [ ] 플로팅 오버레이 형태 위젯 UI 구현 (애니메이션 포함)
- [ ] 메인화면(대화 기록, 로그 뷰) UI 구현
- [ ] 프론트엔드 - 파이썬 백엔드 간 통신 인터페이스 (API / WebSocket) 연결
- [ ] 개인정보 보호 로직(화면 내 비밀번호 마스킹 등) 테스트 적용

## Phase 5: Refactoring & Expandability
- [ ] 멀티 운영체제 확장을 고려한 OS 제어 추상화 레이어 도입
- [ ] 모바일 클라이언트 구동을 위한 네트워크 아키텍처 검토
- [ ] 패키징 및 최종 인스톨러(.exe 등) 배포 테스트
