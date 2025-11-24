import os
from pathlib import Path

env_path = Path("backend/.env.local")

# Read current content
if env_path.exists():
    with open(env_path, 'r') as f:
        content = f.read()
else:
    content = ""

# Check if GROQ_API_KEY already exists
if "GROQ_API_KEY" not in content:
    # Add GROQ_API_KEY
    with open(env_path, 'a') as f:
        f.write("\n# Groq LLM API Key (free and fast)\n")
        f.write("GROQ_API_KEY=your_groq_api_key_here\n")
    print("✓ Added GROQ_API_KEY to backend/.env.local")
    print("\nIMPORTANT: Replace 'your_groq_api_key_here' with your actual Groq API key!")
    print("Get one free at: https://console.groq.com/keys")
else:
    print("✓ GROQ_API_KEY already exists in backend/.env.local")

print("\nCurrent .env.local content:")
with open(env_path, 'r') as f:
    print(f.read())
