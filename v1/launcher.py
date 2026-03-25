import uvicorn
import sys
import os
import threading
import webview  # Added for native window support

# PyInstaller path resolution
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    sys.path.append(base_dir)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(base_dir)

from backend.main import app
import langchain_core.prompts
import langchain_core.runnables
import langchain_openai

def run_api():
    """Runs the FastAPI backend in a separate thread."""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

if __name__ == "__main__":
    print("[*] Starting NAVI Native Application...")
    
    # Start API in background thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Create Native GUI Window
    # Pointing to the local FastAPI server
    webview.create_window('NAVI Voice Assistant', 'http://127.0.0.1:8000', width=1024, height=768)
    webview.start()
