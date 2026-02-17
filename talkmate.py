"""
TalkMate AI - A streamlined AI chatbot using TARS personality

Simplified version of TARS-AI-2 focusing purely on AI conversation capabilities.
Stripped of all hardware components (servos, battery, UI) for lightweight deployment.
"""
import os
import sys

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv()

# Add modules directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from modules.module_config import load_config
from modules.module_character import CharacterManager
from modules.module_memory import MemoryManager
from modules.module_llm import LLMManager

def main():
    """Main application entry point."""
    print("=" * 60)
    print("  TalkMate AI - TARS Personality Assistant")
    print("=" * 60)
    print()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Check for API key
    if not config['LLM'].get('api_key') or config['LLM']['api_key'] == 'YOUR_API_KEY_HERE':
        print("\n⚠ WARNING: No API key found!")
        print("Please set your OpenAI API key in one of these ways:")
        print("  1. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("  2. Edit config.ini and replace YOUR_API_KEY_HERE")
        print()
        api_key = input("Or enter your API key now (or press Enter to exit): ").strip()
        if not api_key:
            print("Exiting...")
            return
        config['LLM']['api_key'] = api_key
    
    print()
    
    # Initialize managers
    print("Initializing AI components...")
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
    
    print()
    print("=" * 60)
    print(f"  {char_manager.char_name} is ready to talk!")
    print("=" * 60)
    print()
    print(f"{char_manager.char_name}: {char_manager.char_greeting}")
    print()
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'clear' to see the greeting again.")
    print("-" * 60)
    print()
    
    # Main conversation loop
    while True:
        try:
            user_input = input(f"{config['CHAR']['user_name']}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"\n{char_manager.char_name}: Until next time.")
                break
            
            if user_input.lower() == 'clear':
                print("\n" + "=" * 60)
                print(f"{char_manager.char_name}: {char_manager.char_greeting}")
                print("=" * 60 + "\n")
                continue
            
            # Get AI response
            print(f"\n{char_manager.char_name}: ", end="", flush=True)
            response = llm_manager.get_completion(user_input)
            
            if response:
                print(response)
            else:
                print("I'm having trouble processing that. Could you try again?")
            
            print()
            
        except KeyboardInterrupt:
            print(f"\n\n{char_manager.char_name}: Interrupted. Shutting down.")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("Continuing...\n")

if __name__ == "__main__":
    main()
