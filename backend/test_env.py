import os
from dotenv import load_dotenv

load_dotenv(".env.local")

print("=== Environment Variables ===")
print(f"LIVEKIT_URL: {os.getenv('LIVEKIT_URL')}")
print(f"LIVEKIT_API_KEY: {os.getenv('LIVEKIT_API_KEY')}")
print(f"LIVEKIT_API_SECRET: {os.getenv('LIVEKIT_API_SECRET')}")
print(f"MURF_API_KEY: {os.getenv('MURF_API_KEY')}")
print(f"GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")
print(f"DEEPGRAM_API_KEY: {os.getenv('DEEPGRAM_API_KEY')}")

# Test Murf import
try:
    from livekit.plugins import murf
    print("\n✓ Murf plugin imported successfully")
    print(f"Murf TTS class: {murf.TTS}")
except Exception as e:
    print(f"\n✗ Error importing Murf: {e}")
