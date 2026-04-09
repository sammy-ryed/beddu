"""
Chat Session Manager - Handle multiple chat sessions like ChatGPT
"""
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class ChatSessionManager:
    """Manages multiple chat sessions for the user."""
    
    def __init__(self, sessions_file: str = "memory/chat_sessions.json"):
        """Initialize the chat session manager."""
        self.sessions_file = sessions_file
        self.sessions = []
        self.current_session_id = None
        self.load_sessions()
        
        # Create a default session if none exist
        if not self.sessions:
            self.create_session("New Chat")
    
    def load_sessions(self):
        """Load all chat sessions from file."""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sessions = data.get('sessions', [])
                    self.current_session_id = data.get('current_session_id')
                    
                    # If no current session, set to the most recent one
                    if not self.current_session_id and self.sessions:
                        self.current_session_id = self.sessions[0]['id']
            except Exception as e:
                print(f"Error loading sessions: {e}")
                self.sessions = []
    
    def save_sessions(self):
        """Save all chat sessions to file."""
        try:
            os.makedirs(os.path.dirname(self.sessions_file), exist_ok=True)
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'sessions': self.sessions,
                    'current_session_id': self.current_session_id
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def create_session(self, title: str = None) -> str:
        """Create a new chat session."""
        session_id = str(uuid.uuid4())
        
        # Auto-generate title if not provided
        if not title:
            title = f"Chat {len(self.sessions) + 1}"
        
        new_session = {
            'id': session_id,
            'title': title,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_message_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'message_count': 0,
            'preview': ''  # First user message
        }
        
        # Add to beginning of list (most recent first)
        self.sessions.insert(0, new_session)
        self.current_session_id = session_id
        self.save_sessions()
        
        return session_id
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all chat sessions."""
        return self.sessions
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a specific session by ID."""
        for session in self.sessions:
            if session['id'] == session_id:
                return session
        return None
    
    def update_session_title(self, session_id: str, title: str):
        """Update the title of a session."""
        for session in self.sessions:
            if session['id'] == session_id:
                session['title'] = title
                self.save_sessions()
                return True
        return False
    
    def update_session_preview(self, session_id: str, preview: str):
        """Update the preview text (first message) of a session."""
        for session in self.sessions:
            if session['id'] == session_id:
                session['preview'] = preview[:100]  # Limit to 100 chars
                session['last_message_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session['message_count'] = session.get('message_count', 0) + 1
                self.save_sessions()
                return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session."""
        for i, session in enumerate(self.sessions):
            if session['id'] == session_id:
                self.sessions.pop(i)
                
                # If deleting current session, switch to another
                if self.current_session_id == session_id:
                    if self.sessions:
                        self.current_session_id = self.sessions[0]['id']
                    else:
                        # Create a new session if all deleted
                        self.create_session("New Chat")
                
                self.save_sessions()
                return True
        return False
    
    def set_current_session(self, session_id: str):
        """Set the active chat session."""
        if self.get_session(session_id):
            self.current_session_id = session_id
            self.save_sessions()
            return True
        return False
    
    def get_current_session_id(self) -> str:
        """Get the current active session ID."""
        return self.current_session_id
    
    def auto_generate_title(self, first_message: str) -> str:
        """Auto-generate a title from the first message."""
        # Take first 5 words or 30 characters, whichever is shorter
        words = first_message.split()[:5]
        title = ' '.join(words)
        if len(title) > 30:
            title = title[:30] + '...'
        return title
