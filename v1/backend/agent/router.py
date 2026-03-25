from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from typing import Literal
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class Intent(BaseModel):
    action: Literal["web_search", "os_control", "general_chat", "none"] = Field(..., description="The type of action to perform")
    target: str = Field(..., description="The target platform or application (e.g. YouTube, Naver Maps, Notepad, or AI)")
    query: str = Field(..., description="The user's search query, command, or message")

SYSTEM_PROMPT = """
You are NAVI, an AI Agent for voice commands. STT often makes phonetic typos in Korean.
BE AGGRESSIVE in mapping typos to the correct action:
1. 'web_search': If user asks for '지드'(Map), '제도'(Map), '유튭', '너튜브', '길찾기' or any search.
   - Example: '네이버 제도' -> target: 'Naver Maps', action: 'web_search'
2. 'os_control': If user asks for '메모 창', '메모 전', '메모 정', '계산 기', '노트패드' or opening apps.
   - Example: '메모 창 켜줘' -> target: 'Notepad', action: 'os_control'
3. 'general_chat': Only for pure greetings like '안녕', '반가워' or simple talk.
4. Otherwise, use 'none'.
Always prioritize mapping to an action over 'general_chat'.
"""

def get_intent(user_input: str):
    # Determine which LLM to use based on environment
    use_local = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    
    if use_local:
        # Local LLM mode (e.g. Ollama, LM Studio)
        local_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434/v1")
        local_model = os.getenv("LOCAL_LLM_MODEL", "llama3")
        print(f"[*] Using Local LLM: {local_model} at {local_url}")
        
        # Point to local server (api_key can be anything for local servers)
        llm = ChatOpenAI(
            model_name=local_model, 
            openai_api_base=local_url,
            openai_api_key="local-placeholder",
            temperature=0
        )
    else:
        # Cloud OpenAI mode
        print("[*] Using Cloud OpenAI Agent")
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        
    try:
        structured_llm = llm.with_structured_output(Intent)
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "{input}")
        ])
        chain = prompt | structured_llm
        return chain.invoke({"input": user_input})
    except Exception as e:
        print(f"[!] LLM Execution Error: {e}")
        # Very simple fallback for offline/local if structured fails
        return Intent(action="none", target="none", query=user_input)

if __name__ == "__main__":
    # Test
    test_inputs = [
        "유튜브에서 고양이 동영상 찾아줘",
        "메모장 열어서 오늘 할 일 작성해",
        "서울역에서 부산역 가는 길찾기"
    ]
    for inp in test_inputs:
        print(f"Input: {inp} -> {get_intent(inp)}")
