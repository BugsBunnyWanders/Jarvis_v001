# Feature Design - Jarvis AI Assistant

## Overview

Jarvis is an interactive AI assistant that can search the web for information, control smart home devices, and answer user questions through a terminal interface or a web API. The system combines research, home automation, and conversational AI to provide helpful responses, and supports both text and voice interaction.

## Architecture

The system consists of four main components:

1. **ResearchAgent**:
   - Uses Google Search API to find information on the web
   - Saves results to a shared state for the main agent to access
   - Uses the Gemini 2.0 Flash model for processing

2. **UtilityAgent**:
   - Controls smart home devices and appliances
   - Provides tools for home automation tasks
   - Handles light control (on/off, color changes, status checks)
   - Uses the Gemini 2.0 Flash model for processing

3. **RootAgent (Jarvis)**:
   - Main interface for user interaction
   - Accesses research results from the shared state
   - Accesses utility agent's capabilities for home automation
   - Presents information to the user in a conversational format
   - Uses the Gemini 2.0 Flash model for processing

4. **API Server**:
   - Flask-based web server that exposes the Jarvis functionality via HTTP
   - Provides endpoints for querying the agent and checking server health
   - Serves a mobile-friendly web interface for interacting with Jarvis
   - Enables access from any device on the local network

## User Flow - Terminal Interface

1. User starts the application from the terminal
2. Application presents a welcome message
3. User types a question or request
4. If information needs to be researched:
   - Research agent performs a Google search
   - Research results are saved to shared state
5. If the user requests a smart home action:
   - Utility agent handles the command (e.g., "turn on the lights")
   - Result of the operation is saved to shared state
6. Main agent formulates a response using the results
7. Response is displayed to the user in the terminal
8. Process repeats until user types 'exit', 'quit', or 'bye'

## User Flow - Web Interface

1. User accesses the web interface from a mobile device or computer
2. Interface displays a welcome message
3. User can interact using:
   - Text: Type a question or request in the input field
   - Voice: Click the microphone button and speak the question
4. Client sends the query to the API server
5. Server processes the query using the Jarvis agent
6. Server returns the response to the client
7. Interface displays the response to the user and can optionally:
   - Read the response aloud using text-to-speech
8. Process repeats until the user closes the interface

## Technical Implementation

- **Session Management**: Uses InMemorySessionService to maintain context
- **State Management**: Shared state between agents using key-value storage
- **Terminal Interface**: Command-line interface with simple input/output
- **Web Interface**: Responsive HTML/CSS/JS interface for mobile devices
- **Voice Interaction**:
  - Speech Recognition: Uses the Web Speech API for voice input
  - Text-to-Speech: Uses the Web Speech Synthesis API for voice output
  - Toggle control for enabling/disabling automatic voice responses
- **Smart Home Control**:
  - Light control: On/off, color changes, status checks
  - Uses TinyTuya library for connecting to smart lights
  - Structured as a tool for the utility agent
- **API Server**: Flask server with JSON endpoints
- **Agent Communication**: AgentTool allows the main agent to call other agents

## API Endpoints

- `GET /`: Serves the web interface
- `GET /api/health`: Health check endpoint
- `POST /api/query`: Main endpoint for querying the agent

## Network Communication

- API server runs on the local machine
- Server binds to all interfaces (0.0.0.0) to allow external access
- Mobile devices can connect via the local network
- Communication uses HTTP for simplicity

## Smart Home Integration

- **Supported Devices**:
  - Smart lights (on/off control, color change)
- **Control Methods**:
  - Direct commands ("Turn on the lights")
  - Color specifications ("Change the light to red")
  - Status queries ("What's the status of the lights?")
- **Implementation**:
  - Uses TinyTuya library for Tuya-compatible devices
  - Provides a clean API for the agent to control devices
  - Error handling for device communication issues

## Future Enhancements

- Add more sophisticated speech recognition capabilities
- Implement persistent session storage for conversation history
- Support for additional smart home devices (fans, thermostats, etc.)
- Add more tool integrations beyond search and home automation
- Create a native mobile app
- Add authentication and user profiles
- Add WebSocket support for real-time updates
- Implement voice customization options (voice selection, speed, pitch)
- Add support for multiple languages for both text and voice interaction 