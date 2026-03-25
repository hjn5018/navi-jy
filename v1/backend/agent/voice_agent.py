import os
import asyncio
import edge_tts
from openai import OpenAI
from typing import Optional

class VoiceAgent:
    """Hybrid Voice Agent supporting Local (Free) and Cloud (OpenAI) STT/TTS."""
    
    def __init__(self):
        # Allow initialization without a key for Local-only mode
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
            print("[!] OPENAI_API_KEY not found. Cloud voice features will be disabled.")
    
    async def text_to_speech(self, text: str, output_path: str = "output.mp3") -> str:
        """Generates voice audio from text."""
        use_local_tts = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
        
        if use_local_tts:
            # Local/Free Mode: Edge-TTS (Microsoft's high quality free engine)
            print(f"[*] Generating speech via Edge-TTS: {text[:30]}...")
            voice = os.getenv("LOCAL_TTS_VOICE", "ko-KR-SunHiNeural")
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            return output_path
        else:
            # Cloud/OpenAI Mode (Requires API Key & Balance)
            print(f"[*] Generating speech via OpenAI TTS: {text[:30]}...")
            try:
                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=text
                )
                response.stream_to_file(output_path)
                return output_path
            except Exception as e:
                print(f"[!] OpenAI TTS Error: {e}. Falling back to Edge-TTS.")
                # Fallback to free edge-tts
                communicate = edge_tts.Communicate(text, "ko-KR-SunHiNeural")
                await communicate.save(output_path)
                return output_path

    async def transcribe_audio(self, audio_path: str) -> str:
        """Converts speech to text (STT) via Cloud or informs that Free STT is browser-side."""
        use_local_stt = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
        
        if use_local_stt:
            # For Local STT, we recommend using Web Speech API in the frontend for performance and size.
            # If server-side offline transcription is strictly required, lighter models (like faster-whisper) 
            # should be installed separately to keep the EXE small.
            print("[*] Local STT requested. For best experience, use browser-side Web Speech API.")
            return "" # Frontend will handle this or send text directly
        else:
            # Cloud/OpenAI Mode (Whisper API)
            print(f"[*] Transcribing via OpenAI Whisper API: {audio_path}")
            try:
                with open(audio_path, "rb") as audio_file:
                    transcript = self.openai_client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        language="ko"
                    )
                return transcript.text
            except Exception as e:
                print(f"[!] OpenAI STT Error: {e}")
                return ""

# Singleton instance
voice_agent = VoiceAgent()

if __name__ == "__main__":
    # Simple test
    async def test():
        agent = VoiceAgent()
        await agent.text_to_speech("반갑습니다. 저는 당신의 AI 비서 나비입니다.", "test.mp3")
    
    asyncio.run(test())
