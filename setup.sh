#!/bin/bash

# ============================================
# E-Shifa AI - Quick Setup Script
# ============================================

echo "🏥 E-Shifa AI - Quick Setup"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites installed${NC}"
echo ""

# ============================================
# Step 1: Setup Database
# ============================================

echo "📊 Step 1: Setting up database..."
echo ""

read -p "Enter PostgreSQL username (default: postgres): " PG_USER
PG_USER=${PG_USER:-postgres}

read -sp "Enter PostgreSQL password: " PG_PASS
echo ""

# Create database
echo "Creating database..."
PGPASSWORD=$PG_PASS psql -U $PG_USER -c "CREATE DATABASE eshifa;" 2>/dev/null || echo "Database already exists"

# Run schema
echo "Running schema..."
PGPASSWORD=$PG_PASS psql -U $PG_USER -d eshifa -f database/mvp_schema.sql

echo -e "${GREEN}✅ Database setup complete${NC}"
echo ""

# ============================================
# Step 2: Setup Backend
# ============================================

echo "🐍 Step 2: Setting up backend..."
echo ""

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Update .env
    sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$PG_USER:$PG_PASS@localhost:5432/eshifa|" .env
    sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
    
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Add your Gemini API key to backend/.env${NC}"
    echo "Get it from: https://makersuite.google.com/app/apikey"
    echo ""
fi

cd ..

echo -e "${GREEN}✅ Backend setup complete${NC}"
echo ""

# ============================================
# Step 3: Setup Frontend
# ============================================

echo "⚛️  Step 3: Setting up frontend..."
echo ""

cd frontend

# Install dependencies
echo "Installing dependencies..."
npm install

# Create .env.local
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.local.example .env.local
fi

cd ..

echo -e "${GREEN}✅ Frontend setup complete${NC}"
echo ""

# ============================================
# Summary
# ============================================

echo "================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Add your Gemini API key to backend/.env"
echo "   Get it from: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Start the frontend (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000"
echo ""
echo "📚 Read START_HERE.md for more details"
echo ""
