import uvicorn
import sys
import os

# PyInstaller path resolution
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    sys.path.append(base_dir)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(base_dir)

from backend.main import app

if __name__ == "__main__":
    print("[*] Starting NAVI All-in-One Service...")
    # Open the browser automatically for the user
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open("http://127.0.0.1:8000")

    Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
