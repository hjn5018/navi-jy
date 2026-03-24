import uiautomation as auto
import subprocess
import time
import os
import webbrowser

class OSAgent:
    """Specialized agent for robust Windows UI Automation and OS control."""
    
    def __init__(self):
        # Set uiautomation common settings
        auto.auto.TimeOut = 5
        
    def open_app(self, app_name: str) -> str:
        """Opens a standard Windows application via subprocess."""
        try:
            print(f"[*] Attempting to open application: {app_name}")
            subprocess.Popen(app_name)
            return f"Successfully opened {app_name}."
        except Exception as e:
            print(f"[!] Failed to open {app_name}: {e}")
            return f"Failed to open {app_name}. (Error: {e})"

    def open_url(self, url: str) -> str:
        """Opens a URL in the default system browser."""
        try:
            print(f"[*] Opening URL: {url}")
            webbrowser.open(url)
            return f"Opened {url} in browser."
        except Exception as e:
            return f"Failed to open URL. (Error: {e})"

    def control_notepad(self, text: str) -> str:
        """Advanced Notepad control for Windows 10/11."""
        try:
            # 1. Open Notepad if not running
            subprocess.Popen('notepad.exe')
            time.sleep(1.5)
            
            # 2. Find the window
            # Win11 Notepad class is often 'Notepad' but name can vary
            window = auto.WindowControl(searchDepth=1, ClassName='Notepad')
            
            if not window.Exists(0):
                # Korean or alternative lookups
                window = auto.WindowControl(searchDepth=1, Name='메모장')
                if not window.Exists(0):
                    window = auto.WindowControl(searchDepth=1, Name='Notepad')

            if window.Exists(0):
                window.SetFocus()
                # Find editable document/edit area
                # Win11: DocumentControl, Win10: EditControl
                edit = window.DocumentControl(searchDepth=3)
                if not edit.Exists(0):
                    edit = window.EditControl(searchDepth=3)
                
                if edit.Exists(0):
                    edit.SendKeys(text)
                    return "Text typed into Notepad successfully."
                return "Could not find Notepad's editing area."
            return "Could not find Notepad window."
        except Exception as e:
            return f"Error controlling Notepad: {e}"

    def control_calculator(self, expression: str = "") -> str:
        """Calculator control scenario."""
        try:
            subprocess.Popen('calc.exe')
            time.sleep(1.5)
            calc = auto.WindowControl(searchDepth=1, Name='계산기') # Korean
            if not calc.Exists(0):
                calc = auto.WindowControl(searchDepth=1, ClassName='ApplicationFrameWindow', Name='Calculator')

            if calc.Exists(0):
                calc.SetFocus()
                if expression:
                    # Type expression directly (most modern calculators support this)
                    calc.SendKeys(expression + '=')
                return "Calculator opened and focus set."
            return "Could not find Calculator window."
        except Exception as e:
            return f"Error controlling Calculator: {e}"

# Singleton implementation
os_agent = OSAgent()

if __name__ == "__main__":
    # Test
    agent = OSAgent()
    # agent.open_app('notepad.exe')
    # agent.control_notepad("Hello from NAVI OS Agent!")
    # agent.control_calculator("123+456")
