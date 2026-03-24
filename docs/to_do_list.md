# NAVI Task To-Do List

## Phase 1: Planning & Design
- [x] PRD (v2.0) 작성 및 기능 명세 확정
- [x] Use Case / Activity 다이어그램 작성 (Mermaid)
- [x] UI/UX 와이어프레임 설계 및 Mockup 제작 (Light Mode)
- [x] 기술 스택 및 초기 아키텍처 확정
- [x] 핵심 DB 스키마(ERD) 정의

## Phase 2: Environment Setup & PoC (Proof of Concept)
- [x] Python 백엔드(FastAPI) 프로젝트 초기화 및 가상환경 세팅
- [x] 프론트엔드/클라이언트 프로젝트 초기화 구축 (Next.js - Light Mockup 디자인 반영)
- [/] OpenAI STT 연동 및 마이크 입력 테스트 스크립트 작성 (스크립트 작성 완료, 통합 대기)
- [ ] GCP TTS 연동 및 스피커 출력 테스트
- [x] Playwright를 이용한 유튜브 자동 검색 파이썬 스크립트(PoC) 작성 (검증 완료)

## Phase 3: Core AI Agent Implementation
- [x] LangChain/기본 프롬프트를 이용한 의도 분석 인텐트 라우터 개발 (gpt-4o-mini structured output)
- [x] 웹 브라우저 탐색 에이전트 구현 (DOM 파싱 및 결과 추출 고도화 - YouTube 연동)
- [x] Windows OS 제어 에이전트 구현 (uiautomation 적용 - 메모장 제어 완료)
- [/] 전체 파이프라인 연동: 음성 입력 -> STT -> 의도 분석 -> Agent 실행 -> 응답 문자열 완성 (통합 완료 및 테스트 환경 구축)

## Phase 4: UI Development & Integration
- [x] 플로팅 오버레이 형태 위젯 UI 구현 (애니메이션 및 Compact 모드 포함)
- [x] 대화형 로그 및 작업 상태 시각화 대시보드 개발 (UI/UX 정교화 완료)
- [x] 백엔드(FastAPI)와 프론트엔드(Next.js) 간 실시간 통신 연동 (WebSocket 기반 실시간 파이프라인 구축 완료)

## Phase 5: Optimization & Deployment
- [x] 개인정보 필터링(Data Masking) 및 보안 로직 적용 (이메일/비밀번호 마스킹 유틸리티 통합)
- [x] 응답 지연 시간(Latency) 최적화 (Playwright 브라우저 싱글톤 패턴 적용)
- [x] 배포 및 자동 실행 단축키 설정 가이드 작성 완료
- [x] **통합 Standalone 배포 (.exe) 빌드 성공** (PyInstaller & Next.js Static Export 적용)
