from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from typing import Literal
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class Intent(BaseModel):
    action: Literal["web_search", "os_control", "none"] = Field(..., description="The type of action to perform")
    target: str = Field(..., description="The target platform or application (e.g. YouTube, Naver Maps, Notepad)")
    query: str = Field(..., description="The user's search query or command")

SYSTEM_PROMPT = """
You are NAVI, an AI Agent assisting users with voice commands.
Analyze the user's intent and select the appropriate action, target, and query.
If the request is about searching videos or directions, use 'web_search'.
If the request is about opening local apps or typing, use 'os_control'.
Otherwise, use 'none'.
"""

def get_intent(user_input: str):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(Intent)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{input}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({"input": user_input})

if __name__ == "__main__":
    # Test
    test_inputs = [
        "유튜브에서 고양이 동영상 찾아줘",
        "메모장 열어서 오늘 할 일 작성해",
        "서울역에서 부산역 가는 길찾기"
    ]
    for inp in test_inputs:
        print(f"Input: {inp} -> {get_intent(inp)}")
