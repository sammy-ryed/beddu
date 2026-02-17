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

    def write_longterm_memory(self, user_input: str, bot_response: str, stress_data: dict = None):
        """Save user input and bot response to conversation history with optional stress data."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": current_time,
            "user_input": user_input,
            "bot_response": bot_response,
        }
        
        # Add stress information if available
        if stress_data:
            entry["stress_detected"] = stress_data.get("stress_level", 0) > 0
            entry["stress_level"] = stress_data.get("stress_level", 0)
            entry["stress_category"] = stress_data.get("category", "none")
            entry["is_crisis"] = stress_data.get("is_crisis", False)
        
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

    def get_stress_statistics(self) -> dict:
        """Calculate stress statistics from conversation history."""
        if not self.conversation_history:
            return {
                "total_sessions": 0,
                "sessions_with_stress": 0,
                "average_stress_level": 0,
                "stress_percentage": 0,
                "recent_avg_stress": 0,
                "previous_avg_stress": 0,
                "improvement_percentage": 0,
                "most_common_category": "none",
                "crisis_count": 0
            }
        
        total_sessions = len(self.conversation_history)
        sessions_with_stress = 0
        total_stress = 0
        crisis_count = 0
        categories = {}
        
        # Split into recent (last 7) and previous (7 before that) for trend analysis
        recent_conversations = self.conversation_history[-7:]
        previous_conversations = self.conversation_history[-14:-7] if len(self.conversation_history) > 7 else []
        
        recent_stress_sum = 0
        recent_stress_count = 0
        previous_stress_sum = 0
        previous_stress_count = 0
        
        # Analyze all conversations
        for entry in self.conversation_history:
            if entry.get("stress_detected", False):
                sessions_with_stress += 1
                stress_level = entry.get("stress_level", 0)
                total_stress += stress_level
                
                category = entry.get("stress_category", "none")
                if category != "none":
                    categories[category] = categories.get(category, 0) + 1
                
                if entry.get("is_crisis", False):
                    crisis_count += 1
        
        # Analyze recent conversations for trend
        for entry in recent_conversations:
            if entry.get("stress_detected", False):
                recent_stress_sum += entry.get("stress_level", 0)
                recent_stress_count += 1
        
        # Analyze previous conversations for comparison
        for entry in previous_conversations:
            if entry.get("stress_detected", False):
                previous_stress_sum += entry.get("stress_level", 0)
                previous_stress_count += 1
        
        # Calculate averages
        average_stress_level = round(total_stress / sessions_with_stress, 2) if sessions_with_stress > 0 else 0
        stress_percentage = round((sessions_with_stress / total_sessions) * 100, 1) if total_sessions > 0 else 0
        
        recent_avg_stress = round(recent_stress_sum / recent_stress_count, 2) if recent_stress_count > 0 else 0
        previous_avg_stress = round(previous_stress_sum / previous_stress_count, 2) if previous_stress_count > 0 else 0
        
        # Calculate improvement (lower stress = positive improvement)
        improvement_percentage = 0
        if previous_avg_stress > 0 and recent_avg_stress > 0:
            improvement_percentage = round(((previous_avg_stress - recent_avg_stress) / previous_avg_stress) * 100, 1)
        
        # Find most common category
        most_common_category = "none"
        if categories:
            most_common_category = max(categories, key=categories.get)
        
        return {
            "total_sessions": total_sessions,
            "sessions_with_stress": sessions_with_stress,
            "average_stress_level": average_stress_level,
            "stress_percentage": stress_percentage,
            "recent_avg_stress": recent_avg_stress,
            "previous_avg_stress": previous_avg_stress,
            "improvement_percentage": improvement_percentage,
            "most_common_category": most_common_category,
            "crisis_count": crisis_count
        }

