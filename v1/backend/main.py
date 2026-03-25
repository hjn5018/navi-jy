from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import json
import os
import base64
from typing import Dict, Any, List
from .agent.manager import manager
from .agent.voice_agent import voice_agent

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
            raw_data = await websocket.receive_text()
            message = json.loads(raw_data)
            
            if message.get("type") == "command":
                user_command = message.get("content")
                await websocket.send_json({"type": "status", "content": "Analyzing intent..."})
                result = await manager.process_command(user_command)
                
                # Check if we should speak the response
                speak_it = message.get("speak", True)
                if speak_it and result.get("status") == "success":
                    ans_text = String(result.get("result", {}).get("content", ""))
                    if ans_text:
                        audio_path = "response.mp3"
                        # Generate speech
                        await voice_agent.text_to_speech(ans_text, audio_path)
                        with open(audio_path, "rb") as f:
                            audio_b64 = base64.b64encode(f.read()).decode()
                        await websocket.send_json({"type": "audio", "content": audio_b64})

                await websocket.send_json({"type": "result", "content": result})

            elif message.get("type") == "audio_input":
                # Process audio data (base64)
                print("[*] Audio data received from client.")
                audio_data = base64.b64decode(message.get("content"))
                tmp_path = "input_voice.webm"
                with open(tmp_path, "wb") as f:
                    f.write(audio_data)
                
                # Transcribe
                transcript = await voice_agent.transcribe_audio(tmp_path)
                print(f"[*] Transcription result: {transcript}")
                
                if transcript.strip():
                    await websocket.send_json({"type": "transcription", "content": transcript})
                    result = await manager.process_command(transcript)
                    await websocket.send_json({"type": "result", "content": result})
                    
                    # Synthesize answer
                    ans_text = String(result.get("result", {}).get("content", ""))
                    if ans_text:
                        audio_path = "response.mp3"
                        await voice_agent.text_to_speech(ans_text, audio_path)
                        with open(audio_path, "rb") as f:
                            audio_b64 = base64.b64encode(f.read()).decode()
                        await websocket.send_json({"type": "audio", "content": audio_b64})
                else:
                    await websocket.send_json({"type": "status", "content": "음성을 인식하지 못했습니다. 다시 말씀해 주세요."})
                    await websocket.send_json({"type": "result", "content": {
                        "status": "error", 
                        "message": "음성 인식 및 변환에 실패했습니다.",
                        "result": {"content": "음성 인식 실패"}
                    }})
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("[!] WebSocket client disconnected.")
    except Exception as e:
        print(f"[!] WebSocket Error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

def String(val: Any) -> str:
    """Safely convert any value to string for TTS."""
    if isinstance(val, dict):
        return json.dumps(val, ensure_ascii=False)
    return str(val)

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
