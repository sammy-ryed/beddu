"""
module_memory.py

Memory Management Module for TalkMate AI.
Handles long-term memory using simple JSON storage (HyperDB disabled due to compatibility issues).
"""
import os
import json
from typing import List
from datetime import datetime

class MemoryManager:
    """Handles memory operations (simple storage) for TalkMate AI."""
    
    def __init__(self, config, char_name, char_greeting):
        self.config = config
        self.char_name = char_name
        self.char_greeting = char_greeting
        self.memory_file = os.path.join(
            os.path.dirname(__file__), '..', 'memory', f"{self.char_name}_conversation.json"
        )
        
        # Load RAG configuration
        rag_config = self.config.get('RAG', {})
        self.top_k = int(rag_config.get('top_k', 5))
        
        # Simple memory storage
        self.conversation_history = []
        self.load_memory()
        
        print(f"✓ Memory system initialized (simple JSON storage)")

    def load_memory(self):
        """Load conversation history from JSON file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.conversation_history = json.load(f)
                print(f"✓ Loaded {len(self.conversation_history)} previous conversations")
            except Exception as e:
                print(f"⚠ Could not load memory: {e}")
                self.conversation_history = []
        else:
            print(f"✓ Creating new memory file")
            self.conversation_history = []
            self.save_memory()

    def save_memory(self):
        """Save conversation history to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            print(f"⚠ Could not save memory: {e}")

    def write_longterm_memory(self, user_input: str, bot_response: str):
        """Save user input and bot response to conversation history."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": current_time,
            "user_input": user_input,
            "bot_response": bot_response,
        }
        self.conversation_history.append(entry)
        # Keep only last 50 conversations
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        self.save_memory()

    def get_related_memories(self, query: str) -> str:
        """Retrieve recent conversations as context."""
        if not self.conversation_history:
            return ""
        
        # Return last 5 conversations
        recent = self.conversation_history[-self.top_k:]
        formatted_memories = []
        for entry in recent:
            formatted_memories.append(
                f"User: {entry['user_input']}\n{self.char_name}: {entry['bot_response']}"
            )
        return "\n\n".join(formatted_memories)

    def get_longterm_memory(self, query: str) -> str:
        """Get recent conversation history."""
        return self.get_related_memories(query)
