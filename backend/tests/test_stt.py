import os
import openai
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(file_path: str):
    """Simple test script for Whisper STT from a local audio file."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

if __name__ == "__main__":
    # Ensure you have a sample audio file to test: e.g. tests/sample.mp3
    # This is a placeholder for development.
    print("STT transcription test ready.")
