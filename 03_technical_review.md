# Navi 기술 검토 및 의사결정

## 1. 기존 계획 검토 결과

사용자의 기존 기획을 검토한 결과, 전체적인 방향은 **매우 타당**하다.  
다만 몇 가지 보완/수정이 필요한 지점이 있다.

---

## 2. 아키텍처 검토

### ✅ 유지할 사항

| 항목 | 판단 | 근거 |
|------|------|------|
| Flutter 프론트엔드 | ✅ 유지 | Windows Desktop 지원 우수, 기존 24일간의 구현 자산 존재 |
| FastAPI 백엔드 | ✅ 유지 | Python 생태계 활용 (LLM, 자동화 도구), 비동기 지원 |
| Playwright 브라우저 자동화 | ✅ 유지 | 기존 Pattern Executor가 잘 동작, 안정적 |
| Pattern Task 아키텍처 | ✅ 유지 | Legacy JSON Plan보다 우수한 구조, 이미 검증됨 |
| 시스템 트레이 구조 | ✅ 유지 | 시각장애인 UX에 적합 |

### ⚠️ 수정이 필요한 사항

#### 2.1 "Frontend가 직접 Playwright를 실행" → 수정 필요

> 기존 기획: "frontend가 직접 playwright나 자동화 도구를 이용해서 조작할 수 있도록 코드를 제공"

**문제점**:
- Flutter는 Dart 기반이므로 Playwright(Node.js/Python)를 직접 실행할 수 없다
- LLM이 Playwright 코드를 생성하면 코드 품질이 불안정하다

**이미 해결된 부분**:
- 현재 프로젝트는 이미 **로컬 Python 서버(local_server)** 를 통해 자동화를 실행하는 구조
- Flutter → Python subprocess/HTTP → Playwright 실행 체인이 구축되어 있음

**권장 수정**:
```
기존 기획:  LLM → Playwright 코드 생성 → Frontend 직접 실행
수정 방향:  LLM → Pattern Task JSON 생성 → Local Python Engine이 실행
```

> [!IMPORTANT]
> LLM은 **코드를 생성하지 않는다**. 대신 `task_type + slots`만 반환하고, 
> 로컬 Pattern Executor가 현재 화면을 보고 실행한다.
> 이 구조가 이미 구현되어 있으므로 그대로 유지하는 것이 최선이다.

#### 2.2 Agent 전략 구체화

> 기존 기획: "하나의 agent를 통해 올바른 코드를 받아 실행하면 좋겠지만, 불가능하다면 sub-agent를 두어서 하네싱을 하거나 온톨로지 기법"

**수정 방향 — 단계적 접근**:

| 단계 | 구조 | 시기 | 설명 |
|------|------|------|------|
| **Phase 1** | 단일 Agent | 즉시 | 하나의 LLM 호출로 Pattern Task JSON 생성. 현재 IntentParser 구조 확장 |
| **Phase 2** | Router + 전문 Agent | 중기 | 브라우저/앱/대화 각 전문 Agent 분리. Router가 분류 |
| **Phase 3** | 온톨로지 + Agent | 장기 | 작업 유형을 계층적 온톨로지로 관리, 확장성 극대화 |

> [!TIP]
> Phase 1의 단일 Agent로 시작하되, Pattern Task의 `task_type`을 온톨로지 노드처럼 설계해두면 
> Phase 3 전환이 자연스럽다. 현재 `keyword_search`, `paired_lookup` 등이 이미 그 역할을 하고 있다.

#### 2.3 Windows 앱 자동화 — 새로운 task_type 계열 필요

기존 Pattern Task는 **브라우저 전용**이다. Windows 앱 자동화를 위해 새로운 task_type 계열이 필요하다.

```json
// 브라우저 자동화 (기존)
{
  "task_type": "keyword_search",
  "domain": "browser"
}

// Windows 앱 자동화 (신규)
{
  "task_type": "app_launch",
  "domain": "windows",
  "slots": {
    "app_name": "메모장"
  }
}

{
  "task_type": "app_input",
  "domain": "windows",
  "slots": {
    "app_name": "메모장",
    "text": "회의 내용 정리"
  }
}
```

**새로 추가할 task_type (Windows 앱 전용)**:

| task_type | 설명 | slots 예시 |
|-----------|------|-----------|
| `app_launch` | 앱 실행 | `{app_name}` |
| `app_close` | 앱 종료 | `{app_name}` |
| `app_input` | 앱 내 텍스트 입력 | `{app_name, text, target_field}` |
| `app_click` | 앱 내 UI 요소 클릭 | `{app_name, element_description}` |
| `app_shortcut` | 앱 내 단축키 실행 | `{app_name, shortcut}` |
| `file_open` | 파일 열기 | `{file_path, app_name}` |
| `file_save` | 파일 저장 | `{app_name, file_path}` |

---

## 3. STT/TTS 기술 선택

### 3.1 STT 비교

| 서비스 | 한국어 | 실시간 | 오프라인 | 비용 | 추천 |
|--------|--------|--------|---------|------|------|
| **Whisper (로컬)** | ⭐⭐⭐ | △ (약간 지연) | ✅ | 무료 | 🥇 1순위 |
| **Google Cloud STT** | ⭐⭐⭐⭐ | ✅ | ❌ | 유료 | 🥈 2순위 |
| **Azure Speech** | ⭐⭐⭐⭐ | ✅ | ❌ | 유료 | 🥉 3순위 |
| **Naver Clova** | ⭐⭐⭐⭐⭐ | ✅ | ❌ | 유료 | 한국어 특화 옵션 |

**권장**: Whisper를 기본으로 사용하고, 정확도가 필요한 경우 Google/Azure로 전환 가능하도록 설계

### 3.2 TTS 비교

| 서비스 | 한국어 품질 | 실시간 | 비용 | 추천 |
|--------|-----------|--------|------|------|
| **Edge TTS** | ⭐⭐⭐⭐ | ✅ | 무료 | 🥇 1순위 |
| **Google Cloud TTS** | ⭐⭐⭐⭐⭐ | ✅ | 유료 | 🥈 2순위 |
| **gTTS** | ⭐⭐⭐ | △ | 무료 | 가벼운 대안 |

**권장**: Edge TTS (무료 + 고품질 한국어)를 기본으로 사용

### 3.3 LLM 비교

| 서비스 | 정확도 | 비용 | 로컬 실행 | 한국어 | 추천 |
|--------|--------|------|----------|--------|------|
| **GPT-4o** | ⭐⭐⭐⭐⭐ | 유료 (중) | ❌ | ⭐⭐⭐⭐ | 🥇 프로덕션 |
| **Claude 3.5 Sonnet** | ⭐⭐⭐⭐⭐ | 유료 (중) | ❌ | ⭐⭐⭐⭐ | 🥈 프로덕션 |
| **Gemini 1.5 Flash** | ⭐⭐⭐⭐ | 유료 (저) | ❌ | ⭐⭐⭐⭐ | 🥉 저비용 |
| **Gemma 2 (로컬)** | ⭐⭐⭐ | 무료 | ✅ | ⭐⭐⭐ | 오프라인용 |
| **Llama 3 (로컬)** | ⭐⭐⭐ | 무료 | ✅ | ⭐⭐ | 오프라인용 |

**권장 전략**:
1. **개발/테스트**: GPT-4o 또는 Gemini Flash (빠른 이터레이션)
2. **프로덕션 기본**: GPT-4o 또는 Claude Sonnet
3. **저비용/오프라인**: Gemma 2 또는 Llama 3 (Ollama로 로컬 실행)
4. **하이브리드**: 간단한 Intent 분류는 로컬 모델, 복잡한 Plan은 유료 모델

---

## 4. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| LLM 응답 불안정 | Pattern Task가 잘못 생성될 수 있음 | Validator Agent 도입, confidence 기반 실행/거절 |
| STT 인식 오류 | 잘못된 명령 실행 위험 | 사용자 확인 절차, "다시 말해줘" 기능 |
| Playwright 사이트 변경 | 기존 바인딩 실패 | Recovery 메커니즘 (이미 구현), Pattern 사전 업데이트 |
| Windows 앱 UI 변경 | pyautogui 좌표 의존 문제 | UI Automation Framework 사용, ARIA/UIA 기반 탐색 |
| 비용 증가 | LLM API 비용 누적 | 로컬 모델 혼합 사용, 캐싱, Intent 분류 경량화 |
| 보안 우려 | 자동화 도구의 악용 가능성 | risk_level 기반 사용자 확인, 민감 작업 차단 |

---

## 5. 결론 — 핵심 수정 사항 요약

1. **LLM은 코드를 생성하지 않는다** → Pattern Task JSON만 반환 (기존 구조 유지)
2. **Agent는 단계적으로 확장** → Phase 1(단일) → Phase 2(Multi) → Phase 3(온톨로지)
3. **Windows 앱 자동화는 별도 domain으로 분리** → `domain: "browser"` vs `domain: "windows"`
4. **STT/TTS는 오프라인 우선** → Whisper(STT) + Edge TTS(TTS) 기본
5. **기존 Pattern Executor 구조를 최대한 재사용** → 24일간의 검증된 구현 자산 활용
