from typing import Dict, Any
from .router import get_intent
from .web_agent import web_agent
from ..poc.notepad_control_uia import uia_notepad_test
from ..utils.security import mask_sensitive_info

class AgentManager:
    """The central brain that coordinates intent analysis and agent execution."""
    
    async def process_command(self, user_input: str) -> Dict[str, Any]:
        # Mask sensitive data for logging
        safe_input = mask_sensitive_info(user_input)
        print(f"[*] Processing user command: {safe_input}")
        
        # 1. Analyze Intent
        try:
            intent = get_intent(user_input) # We send original to LLM for full meaning, but mask the logs
            print(f"[*] Identified Intent: {intent}")
        except Exception as e:
            print(f"[!] Intent analysis failed: {e}")
            return {"status": "error", "message": "Intent analysis failed. Check API Keys."}
        
        # 2. Execute Action based on Intent
        result_data = {}
        
        if intent.action == "web_search":
            if "youtube" in intent.target.lower() or "유튜브" in intent.target:
                print(f"[*] Dispatching to WebAgent: YouTube search for '{intent.query}'")
                result_data["type"] = "web_result"
                result_data["content"] = await web_agent.search_youtube(intent.query)
            else:
                result_data["type"] = "info"
                result_data["content"] = f"Web search for '{intent.target}' is not fully implemented yet."
                
        elif intent.action == "os_control":
            if "notepad" in intent.target.lower() or "메모장" in intent.target:
                print(f"[*] Dispatching to OSAgent: Notepad control for '{intent.query}'")
                # uia_notepad_test is synchronous in current PoC, we can run in thread or make async later
                uia_notepad_test(intent.query)
                result_data["type"] = "os_result"
                result_data["content"] = "Notepad controlled successfully."
            else:
                result_data["type"] = "info"
                result_data["content"] = f"OS control for '{intent.target}' is not fully implemented yet."
        
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
