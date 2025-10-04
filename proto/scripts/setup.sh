#!/bin/bash
# Setup script for Fruit Ninja CV prototype

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Get the project root (parent of scripts directory)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

cd "$PROJECT_ROOT"

echo "================================"
echo "Fruit Ninja CV - Setup Script"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Supabase credentials."
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv package manager..."
    uv sync
else
    echo "Using pip..."
    pip install -e .
fi

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Configure Supabase (interactive):"
echo "   python scripts/setup_supabase.py"
echo ""
echo "2. Or manually edit .env file with your credentials"
echo "   See: docs/SUPABASE_SETUP.md for instructions"
echo ""
echo "3. Run the game:"
echo "   python main.py --player-name 'YourName'"
echo ""
