# TalkMate AI

A streamlined AI chatbot using the TARS personality from the original TARS-AI-2 project. This is a lightweight, conversation-focused version that strips out all hardware components (servos, battery sensors, UI) and keeps only the AI personality and memory systems.

## Features

- 🤖 **TARS Personality**: Full personality system with adjustable parameters (honesty, humor, discretion, etc.)
- 🧠 **Long-term Memory**: Uses HyperDB for context-aware conversations with memory retrieval
- 💬 **Character Cards**: JSON-based character definition system
- 🎯 **Focused & Lightweight**: No hardware dependencies, runs anywhere Python runs
- 🔌 **OpenAI Compatible**: Works with OpenAI API, local LLMs (Ollama, LM Studio), or any OpenAI-compatible endpoint

## Quick Start

### 1. Set up Virtual Environment (Recommended)

```bash
# Navigate to the TalkMate-AI directory
cd TalkMate-AI

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the TalkMate-AI directory:

```bash
OPENAI_API_KEY=your_api_key_here
```

Or edit `config.ini` directly and replace `YOUR_API_KEY_HERE` with your actual API key.

### 4. Run

```bash
python talkmate.py
```

## Configuration

### `config.ini`

- **[CHAR]**: Character and user settings
  - `character_card_path`: Path to character JSON file
  - `user_name`: Your name in the conversation
  
- **[LLM]**: Language model settings
  - `llm_backend`: `openai` (or `ooba`, `tabby` for local)
  - `base_url`: API endpoint
  - `openai_model`: Model to use (e.g., `gpt-4o-mini`)
  - `temperature`, `top_p`, `max_tokens`: Generation parameters
  - `systemprompt`, `instructionprompt`: Behavior instructions

- **[RAG]**: Memory retrieval settings
  - `strategy`: `naive` or other HyperDB strategies
  - `top_k`: Number of memories to retrieve
  - `vector_weight`: Balance between semantic and keyword search

### Using Local LLMs

To use a local LLM (Ollama, LM Studio, etc.), edit `config.ini`:

```ini
[LLM]
llm_backend = openai
base_url = http://localhost:11434/v1  # or your LM Studio URL
openai_model = llama3:8b  # or your model name
api_key = not-needed
```

## Character Customization

Edit `character/TARS/TARS.json` to change personality, or create new character folders with their own JSON and persona.ini files.

### Personality Parameters (`persona.ini`)

```ini
[PERSONA]
honesty = 90      # 0-100: How truthful the AI is
humor = 75        # 0-100: Level of wit and jokes
discretion = 80   # 0-100: Tact and diplomacy
loyalty = 100     # 0-100: Commitment to user
efficiency = 95   # 0-100: Directness and conciseness
wit = 85          # 0-100: Clever responses
```

## What Was Kept from TARS-AI-2

✅ **Kept:**
- Character management system
- Long-term memory (HyperDB)
- Personality traits system
- LLM integration
- Prompt building system
- Memory retrieval (RAG)

❌ **Removed:**
- All hardware modules (servos, battery, sensors)
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Computer vision (BLIP)
- Discord bot
- Web UI
- Bluetooth controllers
- Camera modules
- All 3D printer files and CAD

## Virtual Environment Benefits

Using a virtual environment (`venv`):
- ✅ Isolates dependencies from system Python
- ✅ Prevents conflicts with other projects
- ✅ Keeps your system clean
- ✅ Easy to delete and recreate
- ✅ Portable and reproducible

To deactivate the virtual environment:
```bash
deactivate
```

To delete everything (when in TalkMate-AI folder):
```bash
# Just delete the venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

## Project Structure

```
TalkMate-AI/
├── talkmate.py              # Main application
├── config.ini               # Configuration file
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment file
├── modules/
│   ├── module_config.py    # Config loader
│   ├── module_character.py # Character management
│   ├── module_memory.py    # Memory system (HyperDB)
│   ├── module_llm.py       # LLM integration
│   └── module_prompt.py    # Prompt builder
├── character/
│   └── TARS/
│       ├── TARS.json       # Character definition
│       └── persona.ini     # Personality parameters
└── memory/
    ├── initial_memory.json # Seed memories
    └── TARS.pickle.gz     # (Generated) Conversation history
```

## Commands During Chat

- `exit`, `quit`, `bye` - End conversation
- `clear` - Show greeting again
- Just type normally to chat!

## License

Based on TARS-AI-2 project. Check parent directory for original license and attribution.

## Credits

Simplified from the amazing TARS-AI-2 project which includes physical robot hardware and full sensory integration. This version focuses purely on the AI conversation capabilities.
