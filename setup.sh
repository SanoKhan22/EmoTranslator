#!/bin/bash

# EmoTranslator Setup Script
# This script sets up the EmoTranslator application

echo "🎭 Setting up EmoTranslator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version+ is required."
    exit 1
fi

echo "✅ Python $python_version found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env file from example..."
        cp .env.example .env
        echo "⚠️  Please edit .env file and add your OpenAI API key!"
    else
        echo "📝 Creating .env file..."
        cat > .env << EOL
# EmoTranslator Environment Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
MAX_HISTORY_ITEMS=50
MAX_INPUT_CHARACTERS=200
LOG_LEVEL=INFO
EOL
        echo "⚠️  Please edit .env file and add your OpenAI API key!"
    fi
fi

# Run tests if pytest is available
if command -v pytest &> /dev/null; then
    echo "🧪 Running tests..."
    pytest tests/ -v
else
    echo "⚠️  pytest not found, skipping tests"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file and add your OpenAI API key"
echo "2. Run the application with: streamlit run app.py"
echo "3. Open your browser to http://localhost:8501"
echo ""
echo "For more information, see the README.md file"