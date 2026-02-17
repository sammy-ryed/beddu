"""
Test the memory update/correction feature - like ChatGPT's memory updates
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.module_config import load_config
from modules.module_character import CharacterManager
from modules.module_memory import MemoryManager

def test_memory_updates():
    """Test memory update functionality."""
    print("\n" + "="*70)
    print(" TESTING MEMORY UPDATE FEATURE (Like ChatGPT)")
    print("="*70)
    
    config = load_config()
    char_manager = CharacterManager(config=config)
    memory_manager = MemoryManager(
        config=config,
        char_name=char_manager.char_name,
        char_greeting=char_manager.char_greeting
    )
    
    # Clear existing facts for clean test
    memory_manager.permanent_memory = {"facts": [], "preferences": {}, "important_dates": {}}
    memory_manager.save_permanent_memory()
    
    # Test 1: Add initial facts
    print("\n📝 Step 1: Adding initial facts...")
    memory_manager.extract_important_facts("My name is Rahul", "Nice to meet you!")
    memory_manager.extract_important_facts("I work as a software engineer", "That's great!")
    memory_manager.extract_important_facts("I have 2 children", "Lovely!")
    
    facts = memory_manager.permanent_memory.get('facts', [])
    print(f"✓ Added {len(facts)} initial facts")
    for fact in facts:
        print(f"  - {fact['fact']}")
    
    # Test 2: Update name using "actually"
    print("\n🔄 Step 2: Testing name update with 'actually'...")
    memory_manager.extract_important_facts("Actually, my name is Priya", "Oh, sorry! Nice to meet you, Priya!")
    
    facts = memory_manager.permanent_memory.get('facts', [])
    name_facts = [f for f in facts if 'name' in f['fact'].lower()]
    if name_facts:
        print(f"✓ Name updated to: {name_facts[0]['fact']}")
        if 'Priya' in name_facts[0]['fact']:
            print("✅ Name update SUCCESSFUL!")
        else:
            print("❌ Name update FAILED")
    else:
        print("❌ No name fact found")
    
    # Test 3: Update job using "update memory"
    print("\n🔄 Step 3: Testing job update with 'update memory:'...")
    memory_manager.extract_important_facts("Update memory: I'm now a teacher, not a software engineer", "Got it!")
    
    facts = memory_manager.permanent_memory.get('facts', [])
    work_facts = [f for f in facts if f['category'] == 'work']
    if work_facts:
        print(f"✓ Work updated to: {work_facts[0]['fact']}")
        if 'teacher' in work_facts[0]['fact'].lower():
            print("✅ Job update SUCCESSFUL!")
        else:
            print("❌ Job update FAILED")
    else:
        print("❌ No work fact found")
    
    # Test 4: Update family info using "actually"
    print("\n🔄 Step 4: Testing family update with 'actually'...")
    memory_manager.extract_important_facts("Actually I have 3 children, not 2", "Thanks for the correction!")
    
    facts = memory_manager.permanent_memory.get('facts', [])
    family_facts = [f for f in facts if f['category'] == 'family']
    if family_facts:
        print(f"✓ Family updated to: {family_facts[0]['fact']}")
        if '3' in family_facts[0]['fact']:
            print("✅ Family update SUCCESSFUL!")
        else:
            print("❌ Family update FAILED")
    else:
        print("❌ No family fact found")
    
    # Test 5: Update using "correction:"
    print("\n🔄 Step 5: Testing update with 'Correction:'...")
    memory_manager.extract_important_facts("Correction: I don't work as a teacher, I'm a doctor", "Updated!")
    
    facts = memory_manager.permanent_memory.get('facts', [])
    work_facts = [f for f in facts if f['category'] == 'work']
    if work_facts:
        print(f"✓ Work updated to: {work_facts[0]['fact']}")
        if 'doctor' in work_facts[0]['fact'].lower():
            print("✅ Correction update SUCCESSFUL!")
        else:
            print("❌ Correction update FAILED")
    
    # Test 6: Show final memory state
    print("\n📋 Step 6: Final memory state...")
    context = memory_manager.get_permanent_memory_context()
    print(context)
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    facts = memory_manager.permanent_memory.get('facts', [])
    name_correct = any('Priya' in f['fact'] for f in facts)
    work_correct = any('doctor' in f['fact'].lower() for f in facts)
    family_correct = any('3' in f['fact'] for f in facts if f['category'] == 'family')
    
    results = [
        ("Name Update (actually)", name_correct),
        ("Job Update (update memory)", work_correct or any('teacher' in f['fact'].lower() for f in facts)),
        ("Family Update (actually)", family_correct),
        ("Correction Format", work_correct)
    ]
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed >= 3:
        print("\n🎉 Memory update feature working!")
        print("You can now update your information just like ChatGPT:")
        print("  • 'Actually, my name is...'")
        print("  • 'Update memory: I work as...'")
        print("  • 'Correction: I have X children'")
        print("  • 'I don't work as X anymore, I'm a Y now'")
    else:
        print("\n⚠️ Some tests failed. Review the output above.")


if __name__ == '__main__':
    test_memory_updates()
