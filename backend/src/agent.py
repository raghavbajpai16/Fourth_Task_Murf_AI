import logging
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import silero, groq, deepgram, noise_cancellation, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Load tutor content
CONTENT_FILE = Path(__file__).parent.parent.parent / "shared-data" / "day4_tutor_content.json"
tutor_content = []
if CONTENT_FILE.exists():
    with open(CONTENT_FILE, "r") as f:
        tutor_content = json.load(f)
        logger.info(f"Loaded {len(tutor_content)} concepts from {CONTENT_FILE}")
else:
    logger.warning(f"Content file not found: {CONTENT_FILE}")

# Session state
current_mode = None  # 'learn', 'quiz', or 'teach_back'
current_concept = None
current_room = None


# Greeter Agent - Initial agent that routes to learning modes
class GreeterAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly programming tutor. Your job is to help students learn programming concepts through three different modes.
            
            **IMPORTANT: When you first connect, immediately greet the user warmly and introduce yourself.**
            
            Start with: "Hello! Welcome to your Active Recall Coach! I'm Matthew, and I'm here to help you master programming concepts through active learning."
            
            Then explain the three modes:
            1. LEARN mode - You explain programming concepts with examples and analogies (Voice: Matthew)
            2. QUIZ mode - You ask questions to test their knowledge (Voice: Alicia)
            3. TEACH BACK mode - They explain concepts to you and you give feedback (Voice: Ken)
            
            Available concepts:
            - Variables: Containers that store values
            - Loops: Repeat actions multiple times (for loops, while loops)
            - Functions: Reusable blocks of code
            - Conditional Statements: Make decisions (if/else)
            - Arrays and Lists: Collections of multiple values
            
            After introducing the modes, ask: "Which mode would you like to start with today?"
            
            When they choose a mode, use the switch_mode tool.
            
            Keep responses friendly, encouraging, and concise.""",
        )
    
    @function_tool
    async def switch_mode(self, context: RunContext, mode: Annotated[str, "The learning mode: 'learn', 'quiz', or 'teach_back'"]):
        """Switch to a specific learning mode and change the voice persona.
        
        Args:
            mode: The learning mode to switch to ('learn', 'quiz', or 'teach_back')
        """
        global current_mode
        
        # Normalize the mode input - handle spaces, underscores, and case variations
        mode = mode.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Also handle common variations
        if mode in ['teachback', 'teach']:
            mode = 'teach_back'
        
        if mode not in ['learn', 'quiz', 'teach_back']:
            return f"Sorry, '{mode}' is not a valid mode. Please choose 'learn', 'quiz', or 'teach back'."
        
        current_mode = mode
        logger.info(f"✓ Switching to mode: {mode}")
        
        # Note: Murf TTS voice is set at session start and cannot be changed dynamically
        # We use text-based personas instead to differentiate modes
        
        # Return confirmation message with personalized greeting
        if mode == 'learn':
            return """Hello! I'm Matthew, your learning guide. I'm so glad you chose Learn mode! 
                
I'll be explaining programming concepts in a clear, friendly way with lots of examples. Think of me as your patient teacher who's here to make complex ideas simple.

We can explore these topics together:
• Variables - storing and managing data
• Loops - repeating actions efficiently  
• Functions - creating reusable code blocks
• Conditionals - making smart decisions in code
• Arrays - organizing collections of data

What would you like to learn about first?"""
        elif mode == 'quiz':
            return """Hey there! I'm Alicia, and I'm excited to be your quiz master! 
                
Quiz mode is all about testing what you know and helping you discover what you've mastered. Don't worry - I'll be encouraging and supportive throughout!

I can quiz you on:
• Variables
• Loops
• Functions  
• Conditionals
• Arrays

Which topic would you like to be quizzed on? Let's see what you know!"""
        else:  # teach_back
            return """Hi! I'm Ken, your learning coach. Welcome to Teach Back mode!
                
This is where YOU become the teacher! Explaining concepts in your own words is one of the best ways to truly understand them. I'll listen carefully and give you helpful feedback.

You can teach me about:
• Variables
• Loops
• Functions
• Conditionals  
• Arrays

Which concept would you like to explain to me? Take your time and teach me like I'm learning it for the first time!"""
    
    @function_tool
    async def get_concept(self, context: RunContext, concept_id: Annotated[str, "The concept ID: 'variables', 'loops', 'functions', 'conditionals', or 'arrays'"]):
        """Get information about a programming concept.
        
        Args:
            concept_id: The ID of the concept to retrieve
        """
        global current_concept
        
        concept = next((c for c in tutor_content if c['id'] == concept_id.lower()), None)
        if not concept:
            return f"I don't have information about '{concept_id}'. Available concepts are: variables, loops, functions, conditionals, and arrays."
        
        current_concept = concept
        logger.info(f"Retrieved concept: {concept['title']}")
        
        return f"Concept: {concept['title']}\n\nSummary: {concept['summary']}\n\nSample Question: {concept['sample_question']}"


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    global current_room, current_mode, current_concept
    current_room = ctx.room
    
    # Reset session state when starting
    current_mode = None
    current_concept = None
    
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }
    
    logger.info(f"Received job for room: {ctx.room.name}")

    # Create AgentSession with Ryan voice as default (greeter)
    session = AgentSession(
        stt=deepgram.STT(
            model="nova-2",
            language="en-US",
            smart_format=True,
            interim_results=True,
        ),
        llm=groq.LLM(
            model="llama-3.3-70b-versatile",  # Fast and free
            temperature=0.7,
        ),
        tts=murf.TTS(
            voice="en-US-matthew",  # Matthew - default greeter voice (Day 4 spec)
            style="Conversational",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=1),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=False,
    )

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)
    
    @session.on("agent_speech_committed")
    def _on_agent_speech(text: str):
        logger.info(f"Agent speaking: {text[:100]}...")
    
    @session.on("user_speech_committed") 
    def _on_user_speech(text: str):
        logger.info(f"User said: {text}")

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session with Greeter agent
    greeter = GreeterAgent()
    
    await session.start(
        agent=greeter,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
