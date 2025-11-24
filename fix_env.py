import os

def fix_env(path):
    content = ""
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
    
    lines = content.splitlines()
    env_dict = {}
    for line in lines:
        if '=' in line:
            key, val = line.split('=', 1)
            env_dict[key.strip()] = val.strip()
    
    # Force local dev settings
    env_dict['LIVEKIT_URL'] = 'ws://127.0.0.1:7880'
    env_dict['LIVEKIT_API_KEY'] = 'devkey'
    env_dict['LIVEKIT_API_SECRET'] = 'secret'
    
    # Ensure MURF_API_KEY exists (placeholder if not)
    if 'MURF_API_KEY' not in env_dict:
        env_dict['MURF_API_KEY'] = 'your_murf_api_key_here'
        
    with open(path, 'w') as f:
        for k, v in env_dict.items():
            f.write(f"{k}={v}\n")
    print(f"Fixed {path}")

if __name__ == "__main__":
    fix_env('backend/.env.local')
    fix_env('frontend/.env.local')
