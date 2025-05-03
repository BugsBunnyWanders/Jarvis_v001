from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time
import os
from agent import call_agent, APP_NAME, USER_ID, SESSION_ID

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/query', methods=['POST'])
def query_jarvis():
    """
    Endpoint to query the Jarvis agent
    
    Request body should contain a JSON with a 'query' field:
    {
        "query": "Your question to Jarvis"
    }
    
    Returns a JSON with the 'response' field:
    {
        "response": "Jarvis's answer",
        "timestamp": "2023-06-01T12:34:56.789Z"
    }
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    query = data['query']
    try:
        response = call_agent(query)
        return jsonify({
            'response': response,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()) + 'Z'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint to check if the API is running"""
    return jsonify({
        'status': 'healthy',
        'agent': APP_NAME,
        'session_id': SESSION_ID,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()) + 'Z'
    })

if __name__ == '__main__':
    # Create the static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Get the network IP to access from other devices on the same network
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"=" * 50)
    print(f"Starting Jarvis API server...")
    print(f"Access web interface from your phone at: http://{local_ip}:5000")
    print(f"API endpoint available at: http://{local_ip}:5000/api/query")
    print(f"=" * 50)
    
    # Run the Flask development server with the local IP to allow external access
    app.run(host='0.0.0.0', port=5000, debug=True) 