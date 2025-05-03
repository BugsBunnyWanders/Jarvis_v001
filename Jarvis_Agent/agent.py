# jarvis_server.py
import os, time, threading, sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io, asyncio
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

APP_NAME   = "Jarvis"
USER_ID    = "12345"
SESSION_ID = "1223344"

research_agent = LlmAgent(
    name="ResearchAgent",
    model="gemini-2.0-flash",
    instruction="You are a research assistant that can search the web.",
    tools=[google_search],
    output_key="research_results",
)

root_agent = LlmAgent(
    name="RootAgent",
    model="gemini-2.0-flash",
    instruction=("You are Jarvis, a helpful assistant just like in Iron man movie. Your responses should be in the style of Jarvis from the movie. There should be a touch of humour in your responses."
                 "Web results live in state['research_results']."),
    tools=[AgentTool(agent=research_agent)],
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

app = FastAPI(title="Jarvis API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
class TTSRequest(BaseModel):
    text: str

# quick model using Gemini Audio TTS (as of May 2025 preview)
tts_model = GenerativeModel("models/gemini-tts-1")

@app.post("/tts")
async def tts(req: TTSRequest):
    wav_bytes = await asyncio.to_thread(
        lambda: tts_model.generate_audio(req.text, voice="en-US-Standard-F")
    )
    return StreamingResponse(io.BytesIO(wav_bytes),
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
    # `0.0.0.0` so Docker/Cloud Run can expose it
    uvicorn.run("agent:app", host="0.0.0.0", port=8080)
