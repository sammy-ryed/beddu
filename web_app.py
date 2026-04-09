"""
Web Interface for TalkMate AI - Beedu Mental Health Companion
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add modules directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from modules.module_config import load_config
from modules.module_character import CharacterManager
from modules.module_memory import MemoryManager
from modules.module_llm import LLMManager
from modules.module_chat_sessions import ChatSessionManager

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize AI components
print("Initializing AI components...")
config = load_config()
char_manager = CharacterManager(config=config)
memory_manager = MemoryManager(
    config=config,
    char_name=char_manager.char_name,
    char_greeting=char_manager.char_greeting
)
llm_manager = LLMManager(
    config=config,
    character_manager=char_manager,
    memory_manager=memory_manager
)
chat_sessions = ChatSessionManager()
print(f"✓ {char_manager.char_name} is ready!")

@app.route('/')
def index():
    """Main chat interface."""
    return render_template('index.html', 
                          char_name=char_manager.char_name,
                          char_greeting=char_manager.char_greeting)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get AI response
        response = llm_manager.get_completion(user_message)
        
        if not response:
            response = "I'm having trouble processing that. Could you try again?"
        
        return jsonify({
            'response': response,
            'success': True
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    """Get stress statistics."""
    try:
        stats = memory_manager.get_stress_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats-page')
def stats_page():
    """Render stats page."""
    return render_template('stats.html', char_name=char_manager.char_name)

@app.route('/history')
def get_history():
    """Get conversation history."""
    try:
        limit = request.args.get('limit', type=int, default=None)
        history = memory_manager.get_conversation_history(limit)
        return jsonify({
            'history': history,
            'total_count': len(memory_manager.conversation_history),
            'success': True
        })
    except Exception as e:
        print(f"Error in history endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/history-page')
def history_page():
    """Render conversation history page."""
    return render_template('history.html', char_name=char_manager.char_name)

@app.route('/permanent-memory')
def get_permanent_memory():
    """Get permanent memory facts."""
    try:
        return jsonify({
            'permanent_memory': memory_manager.permanent_memory,
            'success': True
        })
    except Exception as e:
        print(f"Error in permanent memory endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================
# Chat Session Management Endpoints
# ============================================================

@app.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all chat sessions."""
    try:
        sessions = chat_sessions.get_all_sessions()
        current_id = chat_sessions.get_current_session_id()
        return jsonify({
            'sessions': sessions,
            'current_session_id': current_id,
            'success': True
        })
    except Exception as e:
        print(f"Error in sessions endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions', methods=['POST'])
def create_session():
    """Create a new chat session."""
    try:
        data = request.get_json() or {}
        title = data.get('title', None)
        session_id = chat_sessions.create_session(title)
        
        return jsonify({
            'session_id': session_id,
            'session': chat_sessions.get_session(session_id),
            'success': True
        })
    except Exception as e:
        print(f"Error creating session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session."""
    try:
        success = chat_sessions.delete_session(session_id)
        return jsonify({
            'success': success,
            'current_session_id': chat_sessions.get_current_session_id()
        })
    except Exception as e:
        print(f"Error deleting session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/<session_id>/switch', methods=['POST'])
def switch_session(session_id):
    """Switch to a different chat session."""
    try:
        success = chat_sessions.set_current_session(session_id)
        if success:
            return jsonify({
                'success': True,
                'current_session_id': session_id
            })
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        print(f"Error switching session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/<session_id>/rename', methods=['POST'])
def rename_session(session_id):
    """Rename a chat session."""
    try:
        data = request.get_json()
        new_title = data.get('title', '').strip()
        
        if not new_title:
            return jsonify({'error': 'Title cannot be empty'}), 400
        
        success = chat_sessions.update_session_title(session_id, new_title)
        return jsonify({'success': success})
    except Exception as e:
        print(f"Error renaming session: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(f"  {char_manager.char_name} Web Interface Starting...")
    print("=" * 60)
    print("\n  🌐 Open your browser to: http://localhost:5000")
    print("  📊 View stats at: http://localhost:5000/stats-page")
    print("\n  Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
