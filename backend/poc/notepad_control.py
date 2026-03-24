import time
import subprocess
from pywinauto import Application

def control_notepad(content: str):
    """PoC for OS Control: Open Notepad, type text, and focus."""
    print("Launching Notepad...")
    # subprocess.Popen('notepad.exe')
    
    # Alternative: Start using Application
    app = Application(backend="uia").start("notepad.exe")
    
    time.sleep(1) # Wait for window
    
    try:
        # Find the window
        # In modern Windows 11, Notepad might behave differently, 'backend="uia"' is usually safer.
        main_window = app.window(title_re=".*메모장.*") # Korean or matching 'Notepad'
        if not main_window.exists():
            main_window = app.window(title_re=".*Notepad.*")
            
        main_window.set_focus()
        
        # In new Notepad, the editing area is often 'RichEditDUI' or similar.
        # But 'type_keys' usually works on the focused window.
        print(f"Typing content: {content}")
        main_window.type_keys(content, with_spaces=True)
        
        print("Success: Text entered into Notepad.")
    except Exception as e:
        print(f"Failed to control Notepad: {e}")

if __name__ == "__main__":
    test_text = "Hello, this is NAVI AI Agent test."
    control_notepad(test_text)
