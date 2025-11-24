@echo off
echo Starting LiveKit Server...
start "LiveKit Server" cmd /k "livekit-server.exe --dev"

echo Waiting for server to initialize...
timeout /t 2

echo Starting Backend Agent...
start "Backend Agent" cmd /k "cd backend && .venv\Scripts\activate && python src/agent.py dev"

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo All services are starting.
echo Please wait a few moments and then open http://localhost:3000 in your browser.
echo.
pause
