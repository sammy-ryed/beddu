# 🚀 Quick Start Guide - Beedu Mental Health Companion

## Setup (First Time Only)

### Step 1: Get Your Free API Key
1. Go to https://console.groq.com/
2. Sign up for a free account
3. Go to API Keys section
4. Create a new API key and copy it

### Step 2: Configure API Key
Create a file named `.env` in the beddu folder with this content:
```
OPENAI_API_KEY=your_groq_api_key_here
```

**OR** edit `config.ini` and replace `YOUR_API_KEY_HERE` with your actual key.

### Step 3: Install Dependencies
Double-click `setup.bat` or run in terminal:
```bash
setup.bat
```

This will:
- Create a virtual environment
- Install all required packages (Flask, OpenAI, etc.)

---

## Running the Application

### Web Interface (Recommended)
```bash
venv\Scripts\activate
python web_app.py
```

Then open in your browser:
- **Chat**: http://localhost:5000
- **Stats**: http://localhost:5000/stats-page

### Terminal Interface (Alternative)
```bash
venv\Scripts\activate
python talkmate.py
```

---

## Testing Stress Detection

Try these messages to see beedu in action:

### Mental Health Stress
- "I feel so anxious and overwhelmed"
- "Everything feels hopeless"
- "I can't stop worrying about everything"

### Financial Stress
- "I'm drowning in debt and don't know what to do"
- "Lost my job and bills are piling up"
- "Facing eviction next month"

### Crisis (⚠️ Test carefully)
- "I don't want to be here anymore"
- The system will provide immediate crisis resources (988 Suicide Lifeline)

### Normal Conversation
- "How are you today?"
- "I need someone to talk to"
- "What's your name?"

---

## Viewing Progress

1. Chat with beedu for a few conversations
2. Go to http://localhost:5000/stats-page
3. See your stress levels and improvement trends

The stats show:
- Total sessions
- Average stress levels
- Improvement percentage (recent vs previous 7 sessions)
- Most common stress category
- Crisis situations detected

---

## Troubleshooting

### "Import flask could not be resolved"
→ Run `setup.bat` to install dependencies

### "API key not found"
→ Make sure you created the `.env` file with your Groq API key

### "Character file not found"
→ Make sure `character/beedu/beedu.json` exists

### Web interface not loading
→ Check if port 5000 is available (or change port in web_app.py)

---

## Project Structure

```
beddu/
├── web_app.py                     # 🌐 Main web interface (START HERE)
├── talkmate.py                    # 💬 Terminal chat (alternative)
├── config.ini                     # ⚙️ Configuration
├── modules/
│   ├── module_stress_detector.py  # 🧠 Stress detection
│   ├── module_resources.py        # 📚 Resource matching
│   └── module_llm.py              # 🤖 AI integration
├── resources/
│   └── support_resources.json     # 🆘 Crisis hotlines & resources
├── templates/
│   ├── index.html                 # Chat UI
│   └── stats.html                 # Statistics dashboard
└── static/
    ├── style.css                  # Styling
    └── script.js                  # Chat functionality
```

---

## Key Features

✅ **Stress Detection**: Automatically detects mental health, financial, and crisis stress using 75+ keywords
✅ **Crisis Response**: Immediate 988 Suicide Lifeline and crisis resources
✅ **Coping Resources**: 20+ resources including therapy links, financial help, coping strategies
✅ **Progress Tracking**: Stats dashboard showing improvement trends
✅ **Always Available**: 24/7 web interface, no downtime

---

## Next Steps

1. ✅ Run `setup.bat` to install dependencies
2. ✅ Get your Groq API key from https://console.groq.com/
3. ✅ Create `.env` file with your API key
4. ✅ Run `python web_app.py`
5. ✅ Open http://localhost:5000 in your browser
6. ✅ Start chatting with beedu!

---

## Support

For issues or questions:
- Check the full [README.md](README.md) for detailed documentation
- Review [config.ini](config.ini) for configuration options
- Inspect [resources/support_resources.json](resources/support_resources.json) for available resources

---

**⚠️ Important**: This is a support tool, not a replacement for professional help. In crisis, call 988 immediately.
