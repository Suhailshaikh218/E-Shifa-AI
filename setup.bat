@echo off
REM ============================================
REM E-Shifa AI - Quick Setup Script (Windows)
REM ============================================

echo.
echo ============================================
echo E-Shifa AI - Quick Setup (Windows)
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed
    exit /b 1
)

REM Check PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not installed
    exit /b 1
)

echo [OK] All prerequisites installed
echo.

REM ============================================
REM Step 1: Setup Database
REM ============================================

echo ============================================
echo Step 1: Setting up database...
echo ============================================
echo.

set /p PG_USER="Enter PostgreSQL username (default: postgres): "
if "%PG_USER%"=="" set PG_USER=postgres

set /p PG_PASS="Enter PostgreSQL password: "

echo Creating database...
psql -U %PG_USER% -c "CREATE DATABASE eshifa;" 2>nul || echo Database already exists

echo Running schema...
psql -U %PG_USER% -d eshifa -f database\mvp_schema.sql

echo [OK] Database setup complete
echo.

REM ============================================
REM Step 2: Setup Backend
REM ============================================

echo ============================================
echo Step 2: Setting up backend...
echo ============================================
echo.

cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    
    REM Generate secret key
    for /f %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i
    
    REM Update .env (manual step needed)
    echo.
    echo [IMPORTANT] Please update backend\.env with:
    echo 1. DATABASE_URL=postgresql://%PG_USER%:%PG_PASS%@localhost:5432/eshifa
    echo 2. SECRET_KEY=%SECRET_KEY%
    echo 3. GEMINI_API_KEY=YOUR_KEY_HERE
    echo.
    echo Get Gemini API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)

cd ..

echo [OK] Backend setup complete
echo.

REM ============================================
REM Step 3: Setup Frontend
REM ============================================

echo ============================================
echo Step 3: Setting up frontend...
echo ============================================
echo.

cd frontend

REM Install dependencies
echo Installing dependencies...
call npm install

REM Create .env.local
if not exist ".env.local" (
    echo Creating .env.local...
    copy .env.local.example .env.local
)

cd ..

echo [OK] Frontend setup complete
echo.

REM ============================================
REM Summary
REM ============================================

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Update backend\.env with your Gemini API key
echo    Get it from: https://makersuite.google.com/app/apikey
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. Start the frontend (in new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000
echo.
echo Read START_HERE.md for more details
echo.
pause
