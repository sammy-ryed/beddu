"""
Web Interface for TalkMate AI - Beedu Mental Health Companion
"""
from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)

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

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(f"  {char_manager.char_name} Web Interface Starting...")
    print("=" * 60)
    print("\n  🌐 Open your browser to: http://localhost:5000")
    print("  📊 View stats at: http://localhost:5000/stats-page")
    print("\n  Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
