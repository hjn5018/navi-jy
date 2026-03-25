# 🛡️ NAVI 설치 및 실행 가이드 (NAVI Setup Guide)

NAVI (Navigation & Voice Interface)는 음성 및 텍스트를 통해 웹 검색과 Windows OS 제어를 자동화하는 AI 에이전트입니다.

## 📋 사전 요구 사항
- Python 3.10 이상
- Node.js 18 이상
- OpenAI API Key (음성 인식 및 의도 분석용)

## 🛠️ 백엔드(FastAPI) 설정
1. `backend` 폴더로 이동합니다.
2. 가상 환경을 활성화합니다:
   ```bash
   # Windows
   ./venv/Scripts/activate
   ```
3. 필요한 패키지를 설치합니다:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. `.env` 파일을 만들고 API 키를 입력합니다.
5. 서버를 실행합니다:
   ```bash
   python main.py
   ```

## 💻 프론트엔드(Next.js) 설정
1. `client` 폴더로 이동합니다.
2. 의존성을 설치합니다:
   ```bash
   npm install
   ```
3. 대시보드를 실행합니다:
   ```bash
   npm run dev
   ```

## ⌨️ 단축키 안내
- **F2**: 음성 인식 시작 / 중지 (보유중인 위젯이 활성화된 상태에서 작동)
- **Enter**: 텍스트 명령 전송
- **우측 상단 로고 클릭**: 컴팩트 모드 / 대시보드 모드 전환

## 🔒 보안 안내
- 모든 로그와 데이터는 `backend/utils/security.py`를 통해 민감 정보가 자동 마스킹 처리됩니다.
