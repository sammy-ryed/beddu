"""
module_prompt.py

Utility module for building prompts for LLM backends.
"""
from datetime import datetime

def build_prompt(user_prompt, character_manager, memory_manager, config):
    """
    Build a dynamically optimized prompt for the LLM backend.
    
    Parameters:
    - user_prompt (str): The user's input prompt.
    - character_manager: The CharacterManager instance.
    - memory_manager: The MemoryManager instance.
    - config (dict): Configuration dictionary.
    
    Returns:
    - str: The formatted prompt for the LLM backend.
    """
    now = datetime.now()
    dtg = f"Current Date: {now.strftime('%m/%d/%Y')}\nCurrent Time: {now.strftime('%H:%M:%S')}\n"
    user_name = config['CHAR']['user_name']
    char_name = character_manager.char_name

    # Construct persona traits
    persona_traits = "\n".join(
        [f"- {trait}: {value}" for trait, value in character_manager.traits.items()]
    )

    # Get relevant memories
    past_memory = clean_text(memory_manager.get_longterm_memory(user_prompt))

    # Build the base prompt
    base_prompt = (
        f"System: {config['LLM']['systemprompt']}\n\n"
        f"### Instruction:\n{inject_dynamic_values(config['LLM']['instructionprompt'], user_name, char_name)}\n\n"
        f"### Interaction Context:\n---\n"
        f"User: {user_name}\n"
        f"Character: {char_name}\n"
        f"{dtg}\n---\n\n"
        f"### Character Details:\n---\n{character_manager.character_card}\n---\n\n"
        f"### {char_name} Settings:\n{persona_traits}\n---\n\n"
    )

    # Add relevant memories
    if past_memory:
        base_prompt += f"### Relevant Past Conversations:\n---\n{past_memory}\n---\n\n"

    # Add example dialogue
    if character_manager.example_dialogue:
        base_prompt += f"### Example Dialogue:\n---\n{clean_text(character_manager.example_dialogue)}\n---\n\n"

    # Add current user input
    final_prompt = base_prompt + f"### Current Conversation:\n{user_name}: {user_prompt}\n{char_name}:"

    final_prompt = inject_dynamic_values(final_prompt, user_name, char_name)

    return clean_text(final_prompt)

def clean_text(text):
    """Clean and format text for inclusion in the prompt."""
    return (
        text.replace("\\\\", "\\")
            .replace("\\n", "\n")
            .replace("\\'", "'")
            .replace('\\"', '"')
            .replace("<END>", "")
            .strip()
    )

def inject_dynamic_values(text, user_name, char_name):
    """Replace dynamic placeholders in text."""
    return (
        text.replace("{user}", user_name)
            .replace("{char}", char_name)
            .replace("{{user}}", user_name)
            .replace("{{char}}", char_name)
    )
