# Jarvis AI Assistant

An interactive AI assistant that can search the web, answer questions, and control smart home devices. Accessible through a terminal interface or a mobile-friendly web interface with voice interaction capabilities.

## Project Structure

```
Jarvis_v001/
├── Jarvis_Agent/
│   ├── agent.py       # Main agent implementation
│   ├── api.py         # Flask API server
│   ├── lightbulb.py   # Smart light control functions
│   └── static/        # Static web files
│       └── index.html # Web interface
├── docs/
│   └── temp/
│       ├── feature-design.md
│       ├── current-state.md
│       ├── changelog.md
│       └── memory.md
└── README.md          # This file
```

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install google-adk google-genai python-dotenv flask flask-cors tinytuya pydub
   ```
3. Create a `.env` file with your API keys

## Usage

### Terminal Interface

Run the interactive agent in the terminal:

```
cd Jarvis_Agent
python agent.py
```

After running the agent, you can:
- Type your questions or commands
- Control your smart lighting (e.g., "Turn on the lights", "Change the light to red")
- Type 'exit', 'quit', or 'bye' to end the conversation

### Web Interface (Mobile-friendly)

Start the API server:

```
cd Jarvis_Agent
python api.py
```

Then:
1. The server will display a URL (e.g., http://192.168.1.100:5000)
2. Open this URL on your phone's browser (must be on the same network)
3. Interact with Jarvis using:
   - **Text**: Type questions in the chat interface
   - **Voice**: Click the microphone button and speak your question
4. Responses will appear in the chat and can be read aloud if auto TTS is enabled

#### Voice Features

- **Voice Input**: Click the microphone button (🎤) to speak your question
- **Voice Output**: Toggle the "Auto TTS" button in the header to enable/disable automatic reading of responses
- **Note**: Voice features require a modern browser with Web Speech API support

## Smart Home Control

Jarvis can control smart lighting devices. You can:

- Turn lights on and off
- Change light colors (RGB)
- Check light status

Example commands:
- "Turn on the lights"
- "Turn off the lights"
- "Change the light color to red"
- "What's the status of the lights?"

## API Endpoints

- `GET /`: Web interface
- `GET /api/health`: Check if server is running
- `POST /api/query`: Query Jarvis
  - Request body: `{"query": "your question here"}`
  - Response: `{"response": "Jarvis's answer", "timestamp": "..."}`

## Features

- Interactive terminal-based chat interface
- Web API for accessing from mobile devices
- Mobile-friendly chat interface
- Voice input using speech recognition
- Voice output using text-to-speech
- Web search functionality using Google Search API
- Smart home control (lighting)
- Research agent for gathering information
- Utility agent for home automation
- Main agent (Jarvis) that presents information to the user
