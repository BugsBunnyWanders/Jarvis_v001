# Changelog

## [Unreleased]

### Added
- Interactive terminal interface for continuous conversation
- User can exit conversation with 'exit', 'quit', or 'bye' commands
- Error handling for keyboard interrupts and API failures
- Thinking animation during agent processing using threading
- Flask-based API server for accessing Jarvis over HTTP
- Mobile-friendly web interface for interacting with Jarvis from any device
- Voice interaction capabilities:
  - Speech recognition for voice input
  - Text-to-speech for voice output
  - Toggle button for enabling/disabling automatic speech
- API endpoints:
  - POST /api/query: Send queries to Jarvis
  - GET /api/health: Check server status
  - GET /: Serve the web interface
- Project documentation structure
  - README.md with setup instructions and usage
  - Feature design documentation
  - Current state tracking
  - Changelog
  - Memory document for learnings
- Smart home integration for light control
  - Added `lightbulb.py` module with functions for bulb control
  - Implemented functions for turning lights on/off, changing colors, and checking status
  - Created specialized tools for the utility agent to control lights
  - Updated utility agent to use the light control tools
  - Added root agent connection to utility agent
- Testing script for lightbulb functionality

### Changed
- Modified agent.py to support interactive mode instead of single query
- Refactored agent code to separate core functionality from UI
- Updated main function to run in interactive loop
- Improved error handling with try/except blocks
- Enhanced user interface with better formatting and thinking animation
- Enhanced web interface with microphone button for voice input
- Implemented multithreading for UI elements
- Refactored lightbulb control from a single multi-purpose tool to separate specialized tools

### Fixed
- Fixed duplicate utility agent reference in root agent tools list
- Fixed issue with default parameter values in Google ADK tool declarations
- Solved "Default value is not supported in function declaration schema" error

### Removed
- Removed hardcoded example query "What is the structure of a GPT?" 

## [0.3.0] - 2023-10-XX

### Added
- Voice interaction capabilities
  - Implemented speech recognition for voice input
  - Added text-to-speech for voice output
  - Added toggle for automatic voice responses

### Fixed
- Microphone button and send button functionality
- Mobile viewport scaling issues
- Input field visibility on iOS devices

## [0.2.0] - 2023-10-XX

### Added
- Flask API server
  - Created API endpoint for querying Jarvis
  - Added health check endpoint
  - Configured server for local network access
- Mobile-friendly web interface
  - Created responsive UI with chat-like interface
  - Implemented real-time thinking indicators
  - Added error handling for connection issues

## [0.1.0] - 2023-10-XX

### Added
- Initial project setup
- Basic agent structure using Google ADK
- ResearchAgent with Google Search capability
- RootAgent (Jarvis) as the main interface
- Interactive terminal interface with input loop
- Error handling for keyboard interrupts and API failures
- Thinking animation during agent processing
- Project documentation
  - README.md
  - feature-design.md
  - current-state.md
  - changelog.md
  - memory.md 