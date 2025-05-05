# jarvis_server.py
import os, time, threading, sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io, asyncio, base64
from google.generativeai import GenerativeModel

load_dotenv()         # keeps your API keys in .env

#######################################################
#  your existing imports & agent construction ↓
#######################################################
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Import the lightbulb functions
from lightbulb import turn_on, turn_off, set_color, get_status

# Define tools for controlling the lightbulb

def light_on() -> str:
    """
    Turn the smart lightbulb on.
    
    Returns:
        str: A message indicating the result of the operation
    """
    try:
        turn_on()
        return "Light turned on successfully."
    except Exception as e:
        raise Exception(f"Error turning light on: {str(e)}")


def light_off() -> str:
    """
    Turn the smart lightbulb off.
    
    Returns:
        str: A message indicating the result of the operation
    """
    try:
        turn_off()
        return "Light turned off successfully."
    except Exception as e:
        raise Exception(f"Error turning light off: {str(e)}")

def light_color(red: int, green: int, blue: int) -> str:
    """
    Set the light bulb color using RGB values
    
    Args:
        red (int): Red component (0-255)
        green (int): Green component (0-255)
        blue (int): Blue component (0-255)
    
    Returns:
        str: A message indicating the result of the operation
    """
    try:
        # Validate color values
        if not all(0 <= c <= 255 for c in (red, green, blue)):
            raise Exception("RGB values must be between 0 and 255.")
        
        set_color(red, green, blue)
        return f"Light color set to RGB({red}, {green}, {blue})."
    except Exception as e:
        raise Exception(f"Error setting light color: {str(e)}")

def light_status() -> str:
    """
    Get the current status of the light bulb
    
    Returns:
        str: The current status of the light
    """
    try:
        status = get_status()
        return f"Current light status: {status}"
    except Exception as e:
        raise Exception(f"Error checking light status: {str(e)}")

APP_NAME   = "Jarvis"
USER_ID    = "12345"
SESSION_ID = "1223344"

utility_agent = LlmAgent(
    name="UtilityAgent",
    model="gemini-2.0-flash",
    instruction="You are a utility assistant that can help with tasks involving home automation. This can control home appliances and devices like lights, fans, etc.",
    tools=[light_on, light_off, light_color, light_status],
    output_key="utility_results",
)

research_agent = LlmAgent(
    name="ResearchAgent",
    model="gemini-2.0-flash",
    instruction="You are a research assistant that can search the web.",
    description="Does research, and has web search tool at its disposal.",
    tools=[google_search],
    output_key="research_results",
)

root_agent = LlmAgent(
    name="RootAgent",
    model="gemini-2.0-flash",
    instruction=("You are Jarvis, a helpful assistant just like in Iron man movie. Your responses should be in the style of Jarvis from the movie. There should be a touch of humour in your responses."
                 "Web results live in state['research_results']. Utility agent results live in state['utility_results']"),
    description="You are Jarvis, a helpful assistant just like in Iron man movie. Your responses should be in the style of Jarvis from the movie. There should be a touch of humour in your responses.",
    tools=[AgentTool(agent=research_agent), light_on, light_off, light_color, light_status],
)

session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
#######################################################

class Query(BaseModel):
    session_id: str = SESSION_ID  # let caller supply a custom one if they like
    text: str

app = FastAPI(title="Jarvis API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
class TTSRequest(BaseModel):
    text: str

# quick model using Gemini Audio TTS (as of May 2025 preview)
tts_model = GenerativeModel("models/gemini-tts-1")

def synthesis(text: str) -> bytes:
    # Gemini returns base‑64‑encoded WAV.  Decode & re‑encode to MP3.
    wav_b64 = tts_model.generate_audio(text, voice="en-US-Standard-F")
    wav_bytes = base64.b64decode(wav_b64)
    # Re‑encode to MP3 with pydub (ffmpeg); small dependency but worth it
    from pydub import AudioSegment
    mp3_buf = io.BytesIO()
    AudioSegment.from_file(io.BytesIO(wav_bytes), format="wav")\
                .export(mp3_buf, format="mp3", bitrate="128k")
    mp3_buf.seek(0)
    return mp3_buf.read()

@app.post("/tts")
async def tts(req: TTSRequest):
    audio_mp3 = await asyncio.to_thread(synthesis, req.text)
    return StreamingResponse(io.BytesIO(audio_mp3),
                             media_type="audio/mpeg")

@app.post("/chat")
def chat(q: Query):
    content = types.Content(role="user", parts=[types.Part(text=q.text)])

    try:
        events = runner.run(user_id=USER_ID, session_id=q.session_id, new_message=content)
        # Gemini‑2 returns one final message; stream if you prefer
        for ev in events:
            if ev.is_final_response():
                return {"reply": ev.content.parts[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # `0.0.0.0` so Docker/Cloud Run can expose it
    uvicorn.run("agent:app", host="0.0.0.0", port=8080)
