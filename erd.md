# NAVI 프로젝트 ERD (Entity Relationship Diagram)

```mermaid
erDiagram
    USER {
        string user_id PK
        string name "사용자 이름"
        string wake_word "호출명 (e.g. 나비야)"
        string theme "다크모드 / 라이트모드"
        string voice_type "TTS 목소리 종류 (남성/여성 등)"
        datetime created_at
    }

    CONVERSATION {
        string session_id PK
        string user_id FK
        datetime start_time "대화 시작 시간"
        datetime end_time "대화 종료 시간"
    }

    MESSAGE {
        string message_id PK
        string session_id FK
        string role "user | agent | system"
        text content "명령 내용 및 텍스트 응답"
        datetime timestamp "생성 시각"
    }

    ACTION_LOG {
        string log_id PK
        string message_id FK
        string action_type "web_search | os_control | internal_error"
        string target "youtube | naver_map | notepad | system"
        string status "success | fail | pending"
        text masked_data "개인정보가 마스킹 처리된 상세 실행 내역"
        datetime timestamp "수행 시각"
    }

    USER ||--o{ CONVERSATION : "has"
    CONVERSATION ||--o{ MESSAGE : "contains"
    MESSAGE ||--o{ ACTION_LOG : "triggers"
```

## 핵심 테이블 설명
- **USER**: 사용자의 개인화 설정(호출명, 테마, TTS 종류 등)을 저장.
- **CONVERSATION**: 의미 단위의 대화 세션. 예를 들어, 앱이 켜져 있는 동안의 하나의 상호작용 호흡(컨텍스트) 유지.
- **MESSAGE**: 사용자의 STT 결과, 시스템의 내부 메시지, 그리고 NAVI가 돌려주는 텍스트 응답의 로그 체인.
- **ACTION_LOG**: 메시지에 의해 파생된 시스템의 실제 물리적/소프트웨어적 기동 내역을 저장 (보안을 위해 비밀번호 등은 해시나 `***` 형태로 `masked_data`에 저장됨).
