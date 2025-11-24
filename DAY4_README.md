# Day 4: Teach-the-Tutor - Active Recall Coach

## 🎯 Project Overview

An AI-powered Active Recall Coach that helps users master programming concepts through three distinct learning modes. Built with LiveKit Agents, Murf Falcon TTS, and Groq LLM.

## ✨ Features

### Three Learning Modes

1. **LEARN Mode** (Voice: Matthew)
   - Agent explains programming concepts clearly
   - Provides examples and analogies
   - Patient, friendly teaching style

2. **QUIZ Mode** (Voice: Alicia - text persona)
   - Agent asks questions to test knowledge
   - Encouraging and supportive feedback
   - Multiple choice questions

3. **TEACH BACK Mode** (Voice: Ken - text persona)
   - User explains concepts to the agent
   - Agent provides constructive feedback
   - Best way to solidify understanding

### Programming Concepts Covered

- **Variables** - Storing and managing data
- **Loops** - Repeating actions efficiently (for/while loops)
- **Functions** - Creating reusable code blocks
- **Conditionals** - Making smart decisions in code (if/else)
- **Arrays** - Organizing collections of data

## 🏗️ Architecture

### Tech Stack

- **Backend Framework**: LiveKit Agents (Python)
- **LLM**: Groq (llama-3.3-70b-versatile) - Fast and free
- **TTS**: Murf Falcon - Ultra-fast text-to-speech
- **STT**: Deepgram (nova-2 model)
- **VAD**: Silero Voice Activity Detection
- **Frontend**: Next.js + React + LiveKit Components

### Key Components

```
backend/
├── src/
│   └── agent.py          # Main agent logic with GreeterAgent class
├── .env.local            # Environment variables (API keys)
└── pyproject.toml        # Python dependencies

shared-data/
└── day4_tutor_content.json  # Programming concepts content

frontend/
├── app-config.ts         # UI branding and configuration
└── ...                   # Next.js app structure
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- LiveKit Server (for local development)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ten-days-of-voice-agents-2025-main
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env.local
```

Edit `backend/.env.local` with your API keys:

```env
# LiveKit Configuration
LIVEKIT_URL=ws://127.0.0.1:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret

# API Keys
MURF_API_KEY=your_murf_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

**Get Free API Keys:**
- Murf: [https://murf.ai](https://murf.ai)
- Groq: [https://console.groq.com](https://console.groq.com)
- Deepgram: [https://deepgram.com](https://deepgram.com)

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
```

Edit `frontend/.env.local` with the same LiveKit credentials.

### 4. Run the Application

**Option A: Use the batch script (Windows)**

```bash
# From the root directory
.\start_day4.bat
```

**Option B: Run services individually**

```bash
# Terminal 1 - LiveKit Server
.\livekit-server.exe --dev

# Terminal 2 - Backend Agent
cd backend
python src/agent.py start

# Terminal 3 - Frontend
cd frontend
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) in your browser!

## 🎮 How to Use

1. **Start a Session**
   - Click "Start Learning Session"
   - Agent greets you as Matthew

2. **Choose a Mode**
   - Say: "Switch to learn mode"
   - Say: "Switch to quiz mode"
   - Say: "Switch to teach back mode"

3. **Interact with the Agent**
   - **Learn**: Ask to learn about a concept (e.g., "Teach me about variables")
   - **Quiz**: Request a quiz on a topic (e.g., "Quiz me on loops")
   - **Teach Back**: Explain a concept to the agent (e.g., "Let me explain functions")

4. **Switch Modes Anytime**
   - Simply say "Switch to [mode name]" at any time

## 🛠️ Technical Implementation

### Agent Design

The agent uses a single `GreeterAgent` class that handles all three modes:

```python
class GreeterAgent(Agent):
    def __init__(self):
        # Agent instructions and persona
        
    @function_tool
    async def switch_mode(self, context, mode):
        # Handles mode switching with input normalization
        
    @function_tool
    async def get_concept(self, context, concept_id):
        # Retrieves concept information from JSON file
```

### Mode Switching Logic

The agent normalizes user input to handle various formats:
- "teach back" → "teach_back"
- "TEACH BACK" → "teach_back"
- "teachback" → "teach_back"

### Content Management

Concepts are stored in `shared-data/day4_tutor_content.json`:

```json
{
  "id": "variables",
  "title": "Variables",
  "summary": "Variables store values...",
  "sample_question": "What is a variable?"
}
```

## 📊 Performance Optimizations

- **Fast LLM**: Groq's llama-3.3-70b (blazing fast inference)
- **Fast TTS**: Murf Falcon (consistently fastest TTS API)
- **Fast STT**: Deepgram nova-2 model
- **Preemptive Generation**: Enabled for lower latency
- **Interim Results**: STT provides real-time transcription
- **Optimized Turn Detection**: 0.5s min endpointing delay

## 🎯 Day 4 Requirements Checklist

✅ **Primary Goal - Complete**
- [x] Three learning modes (learn, quiz, teach_back)
- [x] Murf Falcon voices (Matthew for all modes, text personas for differentiation)
- [x] JSON content file with programming concepts
- [x] Agent greets user and asks for preferred mode
- [x] Mode switching works at any time
- [x] Content-driven interactions in all modes

## 🐛 Troubleshooting

### Agent Not Responding

1. Check that all API keys are correctly set in `.env.local`
2. Verify LiveKit server is running (`.\livekit-server.exe --dev`)
3. Check backend terminal for errors

### Voice Not Working

1. Ensure `MURF_API_KEY` is valid
2. Check that `text_pacing=True` is set in TTS configuration
3. Verify audio permissions in browser

### Mode Switching Issues

1. Try saying the mode name clearly: "switch to quiz mode"
2. Check backend logs for mode switching confirmation
3. The agent accepts various formats: "teach back", "teachback", etc.

## 📝 Known Limitations

- **Voice Switching**: Murf TTS doesn't support dynamic voice changes mid-session, so all modes use Matthew's voice with distinct text personas
- **Session Persistence**: Conversation state is not saved between sessions

## 🚀 Future Enhancements (Advanced Goals)

Potential improvements for going beyond Day 4:

1. **Mastery Tracking**: Track user performance per concept
2. **Teach-Back Evaluator**: Score user explanations automatically
3. **Learning Paths**: Beginner → Intermediate → Advanced progression
4. **Database Integration**: Persist user progress across sessions
5. **Dynamic Voice Switching**: Implement session restart for voice changes

## 📄 License

This project is part of the Murf AI Voice Agent Challenge.

## 🙏 Acknowledgments

- Built with [LiveKit Agents](https://docs.livekit.io/agents)
- Powered by [Murf Falcon TTS](https://murf.ai)
- LLM by [Groq](https://groq.com)
- STT by [Deepgram](https://deepgram.com)

## 📱 Share Your Work

Complete Day 4 by:
1. Testing all three learning modes
2. Recording a demo video
3. Posting on LinkedIn with:
   - #MurfAIVoiceAgentsChallenge
   - #10DaysofAIVoiceAgents
   - Tag @Murf AI

---

**Built for Day 4 of the Murf AI Voice Agent Challenge** 🎉
