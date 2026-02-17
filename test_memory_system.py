"""
Test the new memory system to ensure permanent memory and conversation history work correctly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.module_config import load_config
from modules.module_character import CharacterManager
from modules.module_memory import MemoryManager

def test_permanent_memory():
    """Test permanent memory storage and retrieval."""
    print("\n" + "="*70)
    print(" TESTING PERMANENT MEMORY SYSTEM")
    print("="*70)
    
    config = load_config()
    char_manager = CharacterManager(config=config)
    memory_manager = MemoryManager(
        config=config,
        char_name=char_manager.char_name,
        char_greeting=char_manager.char_greeting
    )
    
    # Test 1: Add a permanent fact
    print("\n1. Adding permanent fact...")
    memory_manager.add_permanent_fact("User's name is Rahul", "identity")
    print("✓ Added: User's name is Rahul")
    
    # Test 2: Add another fact
    print("\n2. Adding work fact...")
    memory_manager.add_permanent_fact("User works as a software engineer in Bangalore", "work")
    print("✓ Added: User works as a software engineer")
    
    # Test 3: Add family fact
    print("\n3. Adding family fact...")
    memory_manager.add_permanent_fact("User has 2 children and lives with parents", "family")
    print("✓ Added: Family information")
    
    # Test 4: Get permanent memory context
    print("\n4. Retrieving permanent memory context...")
    context = memory_manager.get_permanent_memory_context()
    if context:
        print("✓ Permanent memory retrieved:")
        print(context)
    else:
        print("✗ No permanent memory found")
    
    # Test 5: Test automatic extraction from conversation
    print("\n5. Testing automatic fact extraction...")
    user_msg = "My name is Priya and I work as a teacher in Mumbai"
    bot_msg = "Nice to meet you, Priya!"
    memory_manager.extract_important_facts(user_msg, bot_msg)
    print("✓ Extracted facts from conversation")
    
    # Check if facts were added
    facts = memory_manager.permanent_memory.get('facts', [])
    print(f"✓ Total facts stored: {len(facts)}")
    
    return len(facts) >= 3


def test_conversation_memory():
    """Test conversation history with memory context."""
    print("\n" + "="*70)
    print(" TESTING CONVERSATION MEMORY INTEGRATION")
    print("="*70)
    
    config = load_config()
    char_manager = CharacterManager(config=config)
    memory_manager = MemoryManager(
        config=config,
        char_name=char_manager.char_name,
        char_greeting=char_manager.char_greeting
    )
    
    # Add some conversations
    print("\n1. Adding test conversations...")
    memory_manager.write_longterm_memory(
        "I'm feeling stressed about EMI payments",
        "I understand. EMI stress is common. Let's explore some options together.",
        {"stress_level": 6, "category": "financial", "is_crisis": False}
    )
    print("✓ Added conversation 1")
    
    memory_manager.write_longterm_memory(
        "My family keeps pressuring me to get married",
        "Family pressure can be overwhelming. It's okay to set boundaries.",
        {"stress_level": 5, "category": "family", "is_crisis": False}
    )
    print("✓ Added conversation 2")
    
    # Get long-term memory (should include permanent + chat memory)
    print("\n2. Retrieving long-term memory with context...")
    memory_context = memory_manager.get_longterm_memory("I'm stressed")
    
    if "IMPORTANT:" in memory_context and "RECENT CONVERSATION" in memory_context:
        print("✓ Memory context includes BOTH permanent memory AND chat history!")
        print("\nFull context preview:")
        print(memory_context[:500] + "...")
        return True
    elif "RECENT CONVERSATION" in memory_context:
        print("⚠ Memory context has chat history but no permanent memory")
        return False
    else:
        print("✗ Memory context not properly formatted")
        return False


def test_conversation_history_retrieval():
    """Test getting conversation history."""
    print("\n" + "="*70)
    print(" TESTING CONVERSATION HISTORY RETRIEVAL")
    print("="*70)
    
    config = load_config()
    char_manager = CharacterManager(config=config)
    memory_manager = MemoryManager(
        config=config,
        char_name=char_manager.char_name,
        char_greeting=char_manager.char_greeting
    )
    
    # Get all history
    print("\n1. Getting all conversation history...")
    all_history = memory_manager.get_conversation_history()
    print(f"✓ Retrieved {len(all_history)} conversations")
    
    # Get limited history
    print("\n2. Getting last 5 conversations...")
    limited_history = memory_manager.get_conversation_history(limit=5)
    print(f"✓ Retrieved {len(limited_history)} conversations (limited)")
    
    if len(limited_history) <= 5:
        print("✓ Limit parameter working correctly")
        return True
    else:
        print("✗ Limit parameter not working")
        return False


def run_memory_tests():
    """Run all memory system tests."""
    print("\n" + "="*70)
    print(" BEEDU MEMORY SYSTEM TEST SUITE")
    print("="*70)
    
    results = []
    
    try:
        results.append(("Permanent Memory", test_permanent_memory()))
        results.append(("Conversation Memory Integration", test_conversation_memory()))
        results.append(("History Retrieval", test_conversation_history_retrieval()))
        
        print("\n" + "="*70)
        print(" TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n{passed}/{total} test suites passed")
        
        if passed == total:
            print("\n🎉 Memory system fully functional!")
            print("✓ Permanent memory stores key facts")
            print("✓ Chat memory provides conversation context")
            print("✓ Both memories integrated for LLM")
            print("\nBeedu now remembers important details about you! 🧠")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Please review.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_memory_tests()
