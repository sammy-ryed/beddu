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
        self.permanent_memory_file = os.path.join(
            os.path.dirname(__file__), '..', 'memory', f"{self.char_name}_permanent_memory.json"
        )
        
        # Load RAG configuration
        rag_config = self.config.get('RAG', {})
        self.top_k = int(rag_config.get('top_k', 5))
        
        # Simple memory storage
        self.conversation_history = []
        self.permanent_memory = {}
        self.load_memory()
        self.load_permanent_memory()
        
        print(f"✓ Memory system initialized (conversation + permanent memory)")

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
        
        # Extract important facts for permanent memory
        self.extract_important_facts(user_input, bot_response)

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
        """Get conversation context including permanent memory + recent chat history."""
        context_parts = []
        
        # Add permanent memory first (most important)
        permanent_context = self.get_permanent_memory_context()
        if permanent_context:
            context_parts.append(permanent_context)
        
        # Add recent conversation history
        recent_conversations = self.get_related_memories(query)
        if recent_conversations:
            context_parts.append("\nRECENT CONVERSATION HISTORY:")
            context_parts.append(recent_conversations)
        
        return "\n".join(context_parts) if context_parts else ""

    def load_permanent_memory(self):
        """Load permanent memory (key facts about user) from JSON file."""
        if os.path.exists(self.permanent_memory_file):
            try:
                with open(self.permanent_memory_file, 'r', encoding='utf-8') as f:
                    self.permanent_memory = json.load(f)
                fact_count = len(self.permanent_memory.get('facts', []))
                print(f"✓ Loaded {fact_count} permanent memories")
            except Exception as e:
                print(f"⚠ Could not load permanent memory: {e}")
                self.permanent_memory = {"facts": [], "preferences": {}, "important_dates": {}}
        else:
            self.permanent_memory = {"facts": [], "preferences": {}, "important_dates": {}}
            self.save_permanent_memory()
    
    def save_permanent_memory(self):
        """Save permanent memory to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.permanent_memory_file), exist_ok=True)
            with open(self.permanent_memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.permanent_memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠ Could not save permanent memory: {e}")
    
    def add_permanent_fact(self, fact: str, category: str = "general"):
        """Add a permanent fact about the user."""
        if not fact or len(fact.strip()) < 5:
            return
        
        # Check if fact already exists (avoid duplicates)
        existing_facts = [f['fact'].lower() for f in self.permanent_memory.get('facts', [])]
        if fact.lower() in existing_facts:
            return
        
        fact_entry = {
            "fact": fact,
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mentioned_count": 1
        }
        
        if 'facts' not in self.permanent_memory:
            self.permanent_memory['facts'] = []
        
        self.permanent_memory['facts'].append(fact_entry)
        # Keep only last 50 facts
        if len(self.permanent_memory['facts']) > 50:
            self.permanent_memory['facts'] = self.permanent_memory['facts'][-50:]
        
        self.save_permanent_memory()
        print(f"✓ Remembered: {fact[:60]}...")
    
    def update_permanent_fact(self, old_keyword: str, new_fact: str, category: str = None):
        """Update an existing fact based on keyword match."""
        if 'facts' not in self.permanent_memory:
            self.permanent_memory['facts'] = []
            return False
        
        old_keyword_lower = old_keyword.lower()
        updated = False
        
        # Find and update matching facts
        for i, fact_entry in enumerate(self.permanent_memory['facts']):
            fact_lower = fact_entry['fact'].lower()
            
            # Check if the keyword matches
            if old_keyword_lower in fact_lower:
                # Update the fact
                old_category = fact_entry['category']
                self.permanent_memory['facts'][i] = {
                    "fact": new_fact,
                    "category": category if category else old_category,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "mentioned_count": fact_entry.get('mentioned_count', 1) + 1,
                    "updated_from": fact_entry['fact']  # Keep track of what was changed
                }
                updated = True
                print(f"✓ Updated memory: {fact_entry['fact'][:50]}... → {new_fact[:50]}...")
                break
        
        if updated:
            self.save_permanent_memory()
        
        return updated
    
    def delete_permanent_fact(self, keyword: str):
        """Delete a fact based on keyword match."""
        if 'facts' not in self.permanent_memory:
            return False
        
        keyword_lower = keyword.lower()
        original_count = len(self.permanent_memory['facts'])
        
        # Filter out facts containing the keyword
        self.permanent_memory['facts'] = [
            fact for fact in self.permanent_memory['facts']
            if keyword_lower not in fact['fact'].lower()
        ]
        
        deleted = len(self.permanent_memory['facts']) < original_count
        
        if deleted:
            self.save_permanent_memory()
            print(f"✓ Deleted memory containing: {keyword}")
        
        return deleted
    
    def get_permanent_memory_context(self) -> str:
        """Get permanent memory formatted for LLM context."""
        if not self.permanent_memory or not self.permanent_memory.get('facts'):
            return ""
        
        facts = self.permanent_memory.get('facts', [])
        if not facts:
            return ""
        
        # Group facts by category
        categorized = {}
        for fact_entry in facts:
            category = fact_entry.get('category', 'general')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(fact_entry['fact'])
        
        # Format for context
        context_parts = ["IMPORTANT: Key facts about the user you should remember:"]
        for category, fact_list in categorized.items():
            if fact_list:
                context_parts.append(f"\n{category.upper()}:")
                for fact in fact_list[-10:]:  # Last 10 facts per category
                    context_parts.append(f"  - {fact}")
        
        return "\n".join(context_parts)
    
    def extract_important_facts(self, user_input: str, bot_response: str):
        """Extract and store important facts from conversation (lightweight)."""
        user_lower = user_input.lower()
        
        # PRIORITY: Check for explicit memory update/delete commands
        if any(phrase in user_lower for phrase in [
            "update memory", "update that", "change memory", "correct that",
            "actually", "correction:", "fix that", "not anymore", "no longer"
        ]):
            # Handle explicit updates
            if self._handle_memory_update(user_input, user_lower):
                return  # If update was handled, don't add as new fact
        
        # Check for explicit delete commands
        if any(phrase in user_lower for phrase in [
            "forget that", "delete that", "remove that", "don't remember"
        ]):
            if self._handle_memory_delete(user_input, user_lower):
                return
        
        # Detect name mentions
        if any(phrase in user_lower for phrase in ["my name is", "i'm ", "i am ", "call me"]):
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "am", "i'm", "me"] and i + 1 < len(words):
                    potential_name = words[i + 1].strip('.,!?')
                    if potential_name and potential_name[0].isupper() and len(potential_name) > 1:
                        self.add_permanent_fact(f"User's name is {potential_name}", "identity")
                        break
        
        # Detect occupation
        if any(phrase in user_lower for phrase in ["i work as", "i'm a ", "my job is", "i do ", "working as"]):
            if "work" in user_lower or "job" in user_lower:
                self.add_permanent_fact(f"User mentioned: {user_input[:100]}", "work")
        
        # Detect family mentions (important for India context)
        if any(phrase in user_lower for phrase in ["my family", "my parents", "my spouse", "my children", "my kids"]):
            self.add_permanent_fact(f"Family context: {user_input[:100]}", "family")
        
        # Detect major life events
        if any(phrase in user_lower for phrase in ["got married", "had a baby", "lost my job", "got promoted", "divorced", "moved to"]):
            self.add_permanent_fact(f"Life event: {user_input[:100]}", "life_events")
        
        # Detect recurring financial issues
        if any(phrase in user_lower for phrase in ["emi", "loan", "debt", "salary"]) and "stress" in user_lower:
            self.add_permanent_fact(f"Financial concern: {user_input[:100]}", "financial")
    
    def _handle_memory_update(self, user_input: str, user_lower: str) -> bool:
        """Handle explicit memory update commands."""
        # Pattern 1: "Update memory: <new info>"
        if "update memory:" in user_lower or "update that:" in user_lower:
            parts = user_input.split(":", 1)
            if len(parts) == 2:
                new_info = parts[1].strip()
                # Try to determine what to update based on content
                if self._smart_update(new_info, new_info.lower()):
                    return True
        
        # Pattern 2: "Actually, <new info>" or "Correction: <new info>"
        if user_lower.startswith("actually") or user_lower.startswith("correction"):
            # Extract the corrected information
            if self._smart_update(user_input, user_lower):
                return True
        
        # Pattern 3: Name corrections: "actually my name is X"
        if "actually" in user_lower and ("my name is" in user_lower or "i'm" in user_lower or "i am" in user_lower):
            # Update name
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "am", "i'm"] and i + 1 < len(words):
                    new_name = words[i + 1].strip('.,!?')
                    if new_name and new_name[0].isupper():
                        if not self.update_permanent_fact("name", f"User's name is {new_name}", "identity"):
                            # If no existing name, add it
                            self.add_permanent_fact(f"User's name is {new_name}", "identity")
                        return True
        
        # Pattern 4: Job/work corrections: "i don't work as X anymore" or "i'm now a Y"
        if any(phrase in user_lower for phrase in ["don't work", "no longer work", "not working", "i'm now", "now i'm", "new job", "not a"]):
            if "work" in user_lower or "job" in user_lower or any(word in user_lower for word in ["teacher", "doctor", "engineer", "manager", "developer"]):
                # Update work information - try update first, then add
                if not self.update_permanent_fact("work", f"User mentioned: {user_input[:100]}", "work"):
                    self.add_permanent_fact(f"User mentioned: {user_input[:100]}", "work")
                return True
        
        # Pattern 5: Family corrections
        if "actually" in user_lower and ("children" in user_lower or "kids" in user_lower or "family" in user_lower):
            if not self.update_permanent_fact("family", f"Family context: {user_input[:100]}", "family"):
                # If no existing family fact, add it
                self.add_permanent_fact(f"Family context: {user_input[:100]}", "family")
            return True
        
        return False
    
    def _smart_update(self, text: str, text_lower: str) -> bool:
        """Intelligently determine what category to update based on content."""
        updated = False
        
        # Check for name updates
        if "name" in text_lower:
            words = text.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "am", "i'm"] and i + 1 < len(words):
                    new_name = words[i + 1].strip('.,!?')
                    if new_name and new_name[0].isupper():
                        updated = self.update_permanent_fact("name", f"User's name is {new_name}", "identity")
                        break
        
        # Check for work updates
        if any(word in text_lower for word in ["work", "job", "occupation", "profession"]):
            updated = self.update_permanent_fact("work", f"User mentioned: {text[:100]}", "work")
        
        # Check for family updates
        if any(word in text_lower for word in ["family", "children", "kids", "parents", "spouse"]):
            updated = self.update_permanent_fact("family", f"Family context: {text[:100]}", "family")
        
        # If nothing specific matched, try to add as general update
        if not updated:
            self.add_permanent_fact(f"User update: {text[:100]}", "general")
            updated = True
        
        return updated
    
    def _handle_memory_delete(self, user_input: str, user_lower: str) -> bool:
        """Handle explicit memory delete commands."""
        # Try to extract what to forget
        if "forget that" in user_lower or "delete that" in user_lower:
            # Look at previous context to determine what to delete
            # For now, provide feedback that deletion requires specific keyword
            return False
        
        # Pattern: "forget my name" or "delete my job info"
        keywords_to_delete = []
        if "name" in user_lower:
            keywords_to_delete.append("name")
        if "job" in user_lower or "work" in user_lower:
            keywords_to_delete.append("work")
        if "family" in user_lower:
            keywords_to_delete.append("family")
        
        deleted = False
        for keyword in keywords_to_delete:
            if self.delete_permanent_fact(keyword):
                deleted = True
        
        return deleted
    
    def get_conversation_history(self, limit: int = None) -> list:
        """Get conversation history with optional limit."""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
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

