import uiautomation as auto
import subprocess
import time

def uia_notepad_test(text: str):
    """Notepad control PoC using uiautomation library (more robust for Windows 11/10)."""
    print("Opening Notepad via subprocess...")
    subprocess.Popen('notepad.exe')
    
    # Wait for the window by finding the Notepad window object
    time.sleep(2)
    
    # In Win11, Notepad window title can be "Untitled - Notepad" or similar.
    # We can search by ProcessName if we want to be more specific.
    window = auto.WindowControl(searchDepth=1, ClassName='Notepad')
    
    if not window.Exists(0):
        # Fallback for Win11 style (often class name is 'Notepad')
        print("Standard Notepad class not found, trying different lookup...")
        window = auto.WindowControl(searchDepth=1, Name='메모장') # Korean
        if not window.Exists(0):
            window = auto.WindowControl(searchDepth=1, Name='Notepad') # English
            
    if window.Exists(0):
        print(f"Window found! Setting focus to {window.Name}")
        window.SetFocus()
        
        # Win11 Notepad has a different internal structure (rich edit vs direct)
        # We find the first editable control
        edit = window.DocumentControl(searchDepth=3) # Modern Notepad uses DocumentControl
        if not edit.Exists(0):
            edit = window.EditControl(searchDepth=3) # Legacy Notepad uses EditControl
            
        if edit.Exists(0):
            print("Editing area found! Typing text...")
            edit.SendKeys(text)
            print("Success!")
        else:
            print("Editing area NOT found.")
    else:
        print("Notepad window NOT found.")

if __name__ == "__main__":
    uia_notepad_test("NAVI System: OS Control Test Success (uiautomation)")
