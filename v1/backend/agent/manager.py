from typing import Dict, Any
from .router import get_intent
from .web_agent import web_agent
from .os_agent import os_agent
from ..utils.security import mask_sensitive_info

class AgentManager:
    """The central brain that coordinates intent analysis and agent execution."""
    
    async def process_command(self, user_input: str) -> Dict[str, Any]:
        """Main entry point for command processing."""
        # 1. Mask sensitive data for logging
        safe_input = mask_sensitive_info(user_input)
        print(f"[*] Processing user command: {safe_input}")
        
        # 2. Analyze Intent via LLM
        try:
            intent = get_intent(user_input)
            print(f"[*] Identified Intent: {intent}")
        except Exception as e:
            print(f"[!] Intent analysis failed: {e}. Using fallback.")
            from .router import Intent
            intent = Intent(action="general_chat", target="AI", query=user_input)
        
        # 3. Execute Action based on Intent
        result_data = {}
        target_lower = intent.target.lower()
        
        if intent.action == "web_search":
            # Flexible matching for Korean STT typos
            if any(k in target_lower for k in ["youtube", "유튜브", "너튜브"]):
                print(f"[*] Web search (YouTube) dispatch: {intent.query}")
                result_data["type"] = "web_result"
                result_data["content"] = await web_agent.search_youtube(intent.query)
            elif any(k in target_lower for k in ["map", "지도", "제도", "길찾기"]):
                print(f"[*] Web search (Maps) dispatch: {intent.query}")
                result_data["type"] = "info"
                os_agent.open_url(f"https://map.naver.com/v5/search/{intent.query}")
                result_data["content"] = f"네이버 지도에서 '{intent.query}' 검색 결과로 이동합니다. (인식: {intent.target})"
            else:
                result_data["type"] = "info"
                os_agent.open_url(f"https://www.google.com/search?q={intent.query}")
                result_data["content"] = f"구글에서 '{intent.query}' 검색 결과로 이동합니다."
                
        elif intent.action == "os_control":
            # Flexible matching for Korean STT typos
            if any(k in target_lower for k in ["notepad", "메모장", "메모", "메모 창", "메모 전"]):
                print(f"[*] OS Control (Notepad) dispatch: {intent.query}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.control_notepad(intent.query)
            elif any(k in target_lower for k in ["calc", "계산기", "계산"]):
                print(f"[*] OS Control (Calculator) dispatch: {intent.query}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.control_calculator(intent.query)
            else:
                print(f"[*] OS Control (Open App) fallback: {intent.target}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.open_app(intent.target)
        
        elif intent.action == "general_chat":
            print(f"[*] General Chat dispatch: {intent.query}")
            result_data["type"] = "chat"
            result_data["content"] = f"안녕하세요! 무엇을 도와드릴까요? (인텐트: {intent.query})"
            
        else:
            result_data["type"] = "none"
            result_data["content"] = "죄송해요, 그 요청은 아직 어떻게 처리해야 할지 잘 모르겠어요."
            
        return {
            "status": "success",
            "intent": intent.dict(),
            "result": result_data
        }

# Singleton instance for the app
manager = AgentManager()
