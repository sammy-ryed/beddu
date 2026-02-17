# Beedu Mental Health & Financial Stress Support - MVP Architecture

## 🎯 Project Overview

**Goal**: Transform Beedu into an AI companion that detects mental/financial stress, provides resources, connects to professionals, and tracks improvement over time.

**Target**: Hackathon MVP - Core features only, no advanced ML fine-tuning yet.

---

## 📂 Complete Project Structure

```
beddu/
│
├── config.ini                          [MODIFY] - Add new module configs
├── requirements.txt                    [MODIFY] - Add new dependencies
├── talkmate.py                         [MODIFY] - Main entry point
├── web_app.py                          [MODIFY] - Add dashboard routes
├── .env                                [KEEP] - API keys
│
├── character/
│   ├── TARS/                          [KEEP] - Original character
│   └── beedu/
│       ├── beedu.json                 [MODIFY] - Empathetic mental health persona
│       └── persona.ini                [MODIFY] - Adjust empathy/care traits
│
├── modules/
│   ├── __init__.py                    [KEEP]
│   ├── module_config.py               [KEEP]
│   ├── module_character.py            [KEEP]
│   ├── module_memory.py               [MODIFY] - Enhanced context tagging
│   ├── module_llm.py                  [KEEP]
│   ├── module_prompt.py               [MODIFY] - Add stress context
│   ├── module_stt.py                  [KEEP]
│   ├── module_tts.py                  [KEEP]
│   │
│   ├── module_stress_detector.py      [NEW] - Pattern recognition engine
│   ├── module_financial.py            [NEW] - Financial stress support
│   ├── module_resources.py            [NEW] - Resource recommendation engine
│   ├── module_tracker.py              [NEW] - Mood/stress tracking system
│   └── module_safety.py               [NEW] - Crisis detection & response
│
├── resources/                         [NEW FOLDER]
│   ├── stress_keywords.json           [NEW] - Detection patterns
│   ├── coping_strategies.json         [NEW] - Mental health techniques
│   ├── financial_resources.json       [NEW] - Financial help database
│   ├── professional_help.json         [NEW] - Therapist/advisor links
│   └── crisis_protocols.json          [NEW] - Emergency response rules
│
├── data/                              [NEW FOLDER]
│   ├── mood_history.json              [NEW] - User mood logs
│   ├── stress_events.json             [NEW] - Detected stress patterns
│   └── resource_effectiveness.json    [NEW] - Track what helps
│
├── dashboard/                         [NEW FOLDER]
│   ├── __init__.py                    [NEW]
│   ├── dashboard_app.py               [NEW] - Flask web dashboard
│   ├── templates/
│   │   ├── index.html                 [NEW] - Chat interface
│   │   └── analytics.html             [NEW] - Progress visualization
│   └── static/
│       ├── style.css                  [NEW] - Dashboard styling
│       ├── charts.js                  [NEW] - Chart.js visualizations
│       └── dashboard.js               [NEW] - Frontend logic
│
├── memory/
│   ├── initial_memory.json            [KEEP]
│   ├── beedu_conversation.json        [KEEP] - Conversation history
│   └── stress_context.json            [NEW] - Stress-tagged memories
│
└── static/                            [KEEP] - Existing web assets
    ├── script.js
    └── style.css
```

---

## 🔧 Core Modules Architecture

### **1. Stress Detection Engine**

**File**: `modules/module_stress_detector.py`

**Responsibility**: Analyze conversations for stress indicators

```python
class StressDetector:
    """
    Multi-layer detection system:
    1. Keyword matching - Fast initial scan
    2. Context analysis - Pattern recognition
    3. Severity scoring - 0-10 stress level
    4. Category classification - Mental/Financial/Physical/Social
    """
    
    def detect_stress(self, message, conversation_history):
        """
        Input: User message + history
        Output: {
            'detected': True/False,
            'stress_level': 0-10,
            'categories': ['financial', 'mental'],
            'keywords': ['debt', 'anxious'],
            'severity': 'low|medium|high|crisis',
            'confidence': 0.0-1.0
        }
        """
```

**Data Source**: `resources/stress_keywords.json`

**Integration Point**: Called by `module_llm.py` before generating response

---

### **2. Financial Stress Module**

**File**: `modules/module_financial.py`

**Responsibility**: Detect & address financial stress specifically

```python
class FinancialStressManager:
    """
    Financial stress support:
    - Identify: Debt, unemployment, bills, housing instability
    - Categorize: Emergency vs Long-term financial issues
    - Respond: Suggest budgeting tools, counseling, emergency aid
    """
    
    FINANCIAL_TRIGGERS = [
        'debt', 'bills', 'broke', 'unemployed', 'rent', 
        'eviction', 'bankruptcy', 'loan', 'credit card',
        'can\'t afford', 'no money', 'paycheck', 'laid off'
    ]
    
    def analyze_financial_stress(self, stress_data):
        """
        Input: Stress detection results
        Output: {
            'is_financial': True/False,
            'issue_type': 'debt|unemployment|housing',
            'urgency': 'immediate|short_term|long_term',
            'recommended_resources': [...]
        }
        """
```

**Data Source**: `resources/financial_resources.json`

**Integration Point**: Called after stress detection if financial keywords found

---

### **3. Resource Manager**

**File**: `modules/module_resources.py`

**Responsibility**: Match stress context to appropriate resources

```python
class ResourceManager:
    """
    Context-aware resource provider:
    - Match stress type to resources
    - Prioritize by severity
    - Track resource effectiveness
    """
    
    def get_resources(self, stress_data, user_preferences):
        """
        Input: Stress analysis + user history
        Output: {
            'coping_strategies': [...],
            'professional_help': [...],
            'immediate_actions': [...],
            'long_term_support': [...]
        }
        """
    
    def log_resource_usage(self, resource_id, helpful):
        """Track if resource was helpful for future recommendations"""
```

**Data Sources**: 
- `resources/coping_strategies.json`
- `resources/financial_resources.json`
- `resources/professional_help.json`

**Integration Point**: Called by LLM module to augment AI response

---

### **4. Mood Tracker**

**File**: `modules/module_tracker.py`

**Responsibility**: Log sessions and generate analytics

```python
class MoodTracker:
    """
    Session tracking and progress analytics:
    - Log each conversation
    - Track stress levels over time
    - Identify patterns and triggers
    - Generate progress reports
    """
    
    def log_session(self, session_data):
        """
        Store: {
            'timestamp': '2026-02-17T14:30:00',
            'stress_level': 7,
            'mood': 'anxious',
            'categories': ['financial', 'work'],
            'resources_provided': ['budgeting_guide'],
            'user_feedback': 'helpful'
        }
        """
    
    def get_analytics(self, timeframe='7d'):
        """
        Returns: {
            'stress_trend': [7, 6, 5, 4, 3],  # Last 5 sessions
            'common_triggers': ['work', 'money'],
            'effective_resources': ['breathing_exercises'],
            'improvement_rate': 42.8  # Percentage
        }
        """
```

**Data Storage**: `data/mood_history.json`, `data/stress_events.json`

**Integration Point**: Called at end of each conversation, queried by dashboard

---

### **5. Safety Module**

**File**: `modules/module_safety.py`

**Responsibility**: Crisis detection and emergency response

```python
class SafetyManager:
    """
    Crisis detection and intervention:
    - Detect suicide/self-harm indicators
    - Immediate crisis resource provision
    - Clear boundaries about AI limitations
    """
    
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'end it all', 'not worth living',
        'self harm', 'hurt myself', 'no point', 'better off dead'
    ]
    
    def check_crisis(self, message):
        """
        Output: {
            'is_crisis': True/False,
            'severity': 'immediate|concerning|monitor',
            'action': 'emergency_protocol',
            'resources': ['988_lifeline', '911']
        }
        """
```

**Data Source**: `resources/crisis_protocols.json`

**Integration Point**: Called FIRST before any other processing (highest priority)

---

## 🔄 Data Flow Architecture

### **Conversation Flow (Request → Response)**

```
1. USER INPUT
   ↓
2. SAFETY CHECK (module_safety.py)
   ├─ Crisis detected? → EMERGENCY PROTOCOL → Provide 988/911
   └─ No crisis → Continue
   ↓
3. STRESS DETECTION (module_stress_detector.py)
   ├─ Analyze message + history
   ├─ Detect keywords & patterns
   └─ Output: stress_data
   ↓
4. FINANCIAL ANALYSIS (module_financial.py)
   ├─ If financial keywords found
   └─ Output: financial_context
   ↓
5. RESOURCE MATCHING (module_resources.py)
   ├─ Match stress → resources
   └─ Output: recommended_resources
   ↓
6. PROMPT BUILDING (module_prompt.py)
   ├─ Character persona
   ├─ Conversation history
   ├─ Stress context ← NEW
   ├─ Recommended resources ← NEW
   └─ Output: enriched_prompt
   ↓
7. LLM GENERATION (module_llm.py)
   ├─ Send to Groq (Llama 3.3 70B)
   └─ Output: AI response
   ↓
8. RESPONSE ENHANCEMENT
   ├─ Add resource links
   ├─ Add professional help if needed
   └─ Output: final_response
   ↓
9. TRACKING (module_tracker.py)
   ├─ Log session data
   ├─ Update mood history
   └─ Store for analytics
   ↓
10. DELIVER TO USER
```

---

## 📊 Database Schema (JSON Files)

### **stress_keywords.json**
```json
{
  "mental_health": {
    "anxiety": ["anxious", "panic", "worried", "nervous", "scared"],
    "depression": ["depressed", "hopeless", "worthless", "empty", "numb"],
    "overwhelm": ["overwhelmed", "too much", "can't handle", "breaking down"]
  },
  "financial": {
    "debt": ["debt", "owe", "collections", "bankruptcy"],
    "unemployment": ["unemployed", "lost job", "laid off", "fired"],
    "bills": ["can't pay", "bills", "rent", "eviction", "broke"]
  },
  "physical": {
    "exhaustion": ["exhausted", "tired", "can't sleep", "insomnia"],
    "pain": ["headache", "chest pain", "tense", "stomach ache"]
  }
}
```

### **mood_history.json**
```json
{
  "sessions": [
    {
      "id": "session_001",
      "timestamp": "2026-02-17T14:30:00",
      "stress_level": 7,
      "mood": "anxious",
      "categories": ["financial", "work"],
      "triggers": ["debt", "deadline"],
      "resources_used": ["breathing_exercise", "budget_template"],
      "helpful": true,
      "notes": "User responded well to breathing exercise"
    }
  ]
}
```

### **coping_strategies.json**
```json
{
  "breathing_exercises": {
    "4-7-8": {
      "name": "4-7-8 Breathing",
      "description": "Inhale 4 seconds, hold 7 seconds, exhale 8 seconds",
      "best_for": ["anxiety", "panic", "sleep"],
      "duration": "2-5 minutes"
    }
  },
  "grounding_techniques": {
    "5-4-3-2-1": {
      "name": "5-4-3-2-1 Grounding",
      "description": "Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
      "best_for": ["anxiety", "panic", "overwhelm"]
    }
  },
  "cognitive_techniques": {
    "thought_challenging": {
      "name": "Thought Challenging",
      "description": "Question anxious thoughts: Is this true? What's the evidence?",
      "best_for": ["anxiety", "depression", "negative_thinking"]
    }
  }
}
```

### **financial_resources.json**
```json
{
  "emergency_assistance": {
    "food": {
      "resources": [
        {"name": "Feeding America", "link": "https://feedingamerica.org", "description": "Find local food banks"},
        {"name": "SNAP", "link": "https://www.fns.usda.gov/snap", "description": "Food assistance program"}
      ]
    },
    "housing": {
      "resources": [
        {"name": "211 Helpline", "phone": "211", "description": "Emergency housing assistance"},
        {"name": "HUD Housing Counseling", "link": "https://www.hud.gov", "description": "Rent assistance"}
      ]
    }
  },
  "debt_management": {
    "counseling": [
      {"name": "NFCC", "link": "https://www.nfcc.org", "description": "Nonprofit credit counseling", "cost": "Free or low-cost"}
    ],
    "strategies": [
      {"name": "Debt Snowball", "description": "Pay smallest debts first for motivation"},
      {"name": "Debt Avalanche", "description": "Pay highest interest first to save money"}
    ]
  },
  "budgeting_tools": [
    {"name": "YNAB", "link": "https://youneedabudget.com", "cost": "Paid"},
    {"name": "Mint", "link": "https://mint.com", "cost": "Free"},
    {"name": "50/30/20 Rule", "description": "50% needs, 30% wants, 20% savings"}
  ]
}
```

### **professional_help.json**
```json
{
  "crisis_lines": {
    "988": {
      "name": "988 Suicide & Crisis Lifeline",
      "phone": "988",
      "text": "Text 988",
      "available": "24/7",
      "description": "Free, confidential crisis support"
    },
    "741741": {
      "name": "Crisis Text Line",
      "text": "Text HOME to 741741",
      "available": "24/7"
    }
  },
  "therapy_platforms": {
    "betterhelp": {
      "name": "BetterHelp",
      "link": "https://www.betterhelp.com",
      "cost": "$60-90/week",
      "insurance": false
    },
    "openpath": {
      "name": "Open Path Collective",
      "link": "https://openpathcollective.org",
      "cost": "$30-80/session",
      "description": "Low-cost therapy network"
    }
  },
  "financial_counseling": {
    "nfcc": {
      "name": "National Foundation for Credit Counseling",
      "link": "https://www.nfcc.org",
      "phone": "800-388-2227",
      "cost": "Free or low-cost"
    }
  },
  "support_groups": {
    "nami": {
      "name": "NAMI Support Groups",
      "link": "https://www.nami.org/Support-Education/Support-Groups",
      "cost": "Free"
    }
  }
}
```

---

## 🎨 Dashboard Architecture

### **Flask Web Dashboard** (`dashboard/dashboard_app.py`)

**Routes**:
- `/` - Main chat interface (existing web_app.py)
- `/analytics` - Progress dashboard (NEW)
- `/api/mood-data` - JSON endpoint for chart data
- `/api/stress-history` - Stress level trends

**Analytics Page Features**:
1. **Stress Level Line Chart** - Last 30 days
2. **Category Breakdown** - Pie chart (Mental vs Financial vs Physical)
3. **Resource Effectiveness** - Bar chart (What helped most)
4. **Milestones** - Badge system ("7 days tracked", "Stress reduced 30%")

---

## 🔌 Integration Points

### **Modified Files**

#### **config.ini** - Add new sections
```ini
[STRESS_DETECTION]
enabled = True
keywords_file = resources/stress_keywords.json
min_confidence = 0.6

[TRACKING]
enabled = True
log_sessions = True
history_file = data/mood_history.json

[RESOURCES]
coping_strategies = resources/coping_strategies.json
financial_help = resources/financial_resources.json
professional_help = resources/professional_help.json
```

#### **module_prompt.py** - Add stress context
```python
def build_prompt(user_prompt, character_manager, memory_manager, config, stress_context=None):
    # ... existing code ...
    
    # NEW: Add stress context to prompt
    if stress_context and stress_context['detected']:
        base_prompt += f"\n### Current Stress Context:\n"
        base_prompt += f"Stress Level: {stress_context['stress_level']}/10\n"
        base_prompt += f"Categories: {', '.join(stress_context['categories'])}\n"
        base_prompt += f"Recommended Resources: {stress_context.get('resources', [])}\n"
    
    # ... rest of code ...
```

#### **module_llm.py** - Call stress detector
```python
def get_completion(self, user_prompt):
    # NEW: Check for crisis first
    crisis_check = self.safety_manager.check_crisis(user_prompt)
    if crisis_check['is_crisis']:
        return self._handle_crisis(crisis_check)
    
    # NEW: Detect stress
    stress_data = self.stress_detector.detect_stress(
        user_prompt, 
        self.memory_manager.conversation_history
    )
    
    # NEW: Get resources if stress detected
    if stress_data['detected']:
        resources = self.resource_manager.get_resources(stress_data)
        stress_data['resources'] = resources
    
    # Build prompt with stress context
    prompt = build_prompt(
        user_prompt, 
        self.character_manager, 
        self.memory_manager, 
        self.config,
        stress_context=stress_data  # NEW
    )
    
    # ... existing LLM call ...
    
    # NEW: Track session
    self.tracker.log_session({
        'message': user_prompt,
        'response': bot_reply,
        'stress_data': stress_data
    })
```

---

## 📦 Dependencies to Add

**requirements.txt additions**:
```txt
# Existing dependencies
openai
requests
python-dotenv
tiktoken
hyperdb

# NEW for MVP
flask==3.0.0              # Web dashboard
flask-cors==4.0.0         # CORS for API
matplotlib==3.8.0         # Chart generation
pandas==2.1.0             # Data analysis
```

---

## 🚀 MVP Feature Checklist

### **Core Features (Must Have)**

- [ ] **Stress Detection Engine**
  - [ ] Keyword matching (mental, financial, physical)
  - [ ] Severity scoring (0-10)
  - [ ] Category classification
  
- [ ] **Financial Stress Module**
  - [ ] Financial keyword detection
  - [ ] Budget/debt resource suggestions
  - [ ] Emergency assistance links
  
- [ ] **Resource Management**
  - [ ] Coping strategy database
  - [ ] Professional help database
  - [ ] Context-aware recommendations
  
- [ ] **Crisis Safety**
  - [ ] Crisis keyword detection
  - [ ] Immediate 988/911 provision
  - [ ] Clear AI limitation disclaimers

- [ ] **Mood Tracking**
  - [ ] Session logging
  - [ ] Stress level history
  - [ ] Resource effectiveness tracking

- [ ] **Analytics Dashboard**
  - [ ] Stress level chart (Line graph)
  - [ ] Category breakdown (Pie chart)
  - [ ] Progress indicators

### **Character Updates**

- [ ] Rewrite beedu as empathetic mental health companion
- [ ] Update greeting to check-in style
- [ ] Add stress-aware example dialogues
- [ ] Adjust persona parameters (higher empathy)

---

## ⚡ MVP vs Future Features

### **MVP (What We're Building Now)**
✅ Text-based stress detection  
✅ Resource database & matching  
✅ Mood tracking over time  
✅ Basic analytics dashboard  
✅ Crisis detection & response  

### **Future Enhancements (Post-Hackathon)**
⏳ Voice tone stress analysis (multimodal)  
⏳ Custom model fine-tuning on stress data  
⏳ Federated learning for privacy  
⏳ Mobile app version  
⏳ Integration with therapy scheduling APIs  

---

## 🎯 Success Metrics (For Demo)

1. **Detection Accuracy**: "Correctly identifies stress in 90%+ of test cases"
2. **Response Time**: "Provides resources within 2 seconds"
3. **User Journey**: "From stressed (8/10) to calm (4/10) in one session"
4. **Resource Variety**: "50+ mental health & financial resources"
5. **Tracking Capability**: "Visualizes progress over 7+ days"

---

This MVP architecture is **ready for immediate implementation**. All modules are clearly defined with inputs/outputs, and integration points are specified. Ready to start building?
