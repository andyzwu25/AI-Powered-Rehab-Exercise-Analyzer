@echo off
echo Starting Exercise Form Analyzer with Docker...
echo.

echo Building and starting Backend (Docker)...
docker-compose up --build -d

echo.
echo Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "npm start"

echo.
echo Both servers are starting...
echo Backend (Docker) will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to exit this script...
pause > nul 