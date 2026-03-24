from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import os
from typing import Dict, Any, List
from .agent.manager import manager

app = FastAPI(title="NAVI Agent API")

# List to manage active websocket connections
active_connections: List[WebSocket] = []

# Setup CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

# Path resolution for Standalone EXE (PyInstaller)
import sys
if getattr(sys, 'frozen', False):
    # If the app is run as a bundle (EXE)
    base_path = sys._MEIPASS
    static_path = os.path.join(base_path, 'client', 'out')
else:
    # If run as a normal script
    base_path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(os.path.dirname(base_path), 'client', 'out')

@app.get("/")
def read_root():
    from fastapi.responses import FileResponse
    if os.path.exists(static_path):
        return FileResponse(os.path.join(static_path, 'index.html'))
    return {"status": "NAVI Agent is running (Static Front-end not found)"}

# Static assets (JS/CSS) should be served via /_next or similar
if os.path.exists(static_path):
    app.mount("/_next", StaticFiles(directory=os.path.join(static_path, '_next')), name="next-static")
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("[*] WebSocket client connected.")
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "command":
                user_command = message.get("content")
                # Send initial ACK
                await websocket.send_json({"type": "status", "content": "Analyzing intent..."})
                
                # Process command via AgentManager
                # Note: manager should preferably be updated to support partial updates via callback
                result = await manager.process_command(user_command)
                
                # Send result back
                await websocket.send_json({"type": "result", "content": result})
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("[!] WebSocket client disconnected.")
    except Exception as e:
        print(f"[!] WebSocket Error: {e}")
        active_connections.remove(websocket)

@app.post("/api/command")
async def process_command(request: CommandRequest):
    """Processes user voice/text command through Agent Manager."""
    try:
        # Process asynchronously through AgentManager
        result = await manager.process_command(request.command)
        return result
    except Exception as e:
        print(f"[!] Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use -m to run as a module for proper imports
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
