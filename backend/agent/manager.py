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
            print(f"[!] Intent analysis failed: {e}")
            return {"status": "error", "message": "Failed to analyze intent."}
        
        # 3. Execute Action based on Intent
        result_data = {}
        target_lower = intent.target.lower()
        
        if intent.action == "web_search":
            if "youtube" in target_lower or "유튜브" in intent.target:
                print(f"[*] Web search (YouTube) dispatch: {intent.query}")
                result_data["type"] = "web_result"
                result_data["content"] = await web_agent.search_youtube(intent.query)
            elif "map" in target_lower or "지도" in intent.target:
                print(f"[*] Web search (Maps) dispatch: {intent.query}")
                result_data["type"] = "info"
                # For maps, we just open the URL
                os_agent.open_url(f"https://map.naver.com/v5/search/{intent.query}")
                result_data["content"] = f"Opening Naver Maps for '{intent.query}'."
            else:
                result_data["type"] = "info"
                os_agent.open_url(f"https://www.google.com/search?q={intent.query}")
                result_data["content"] = f"Searching Google for '{intent.query}'."
                
        elif intent.action == "os_control":
            if "notepad" in target_lower or "메모장" in intent.target:
                print(f"[*] OS Control (Notepad) dispatch: {intent.query}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.control_notepad(intent.query)
            elif "calc" in target_lower or "계산기" in intent.target:
                print(f"[*] OS Control (Calculator) dispatch: {intent.query}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.control_calculator(intent.query)
            else:
                # Fallback: Treat target as app name to open
                print(f"[*] OS Control (Open App) fallback: {intent.target}")
                result_data["type"] = "os_result"
                result_data["content"] = os_agent.open_app(intent.target)
        
        else:
            result_data["type"] = "none"
            result_data["content"] = "I'm not sure how to handle that request yet."
            
        return {
            "status": "success",
            "intent": intent.dict(),
            "result": result_data
        }

# Singleton instance for the app
manager = AgentManager()
