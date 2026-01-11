#!/bin/bash

# FactBot Setup Script

echo "Setting up FactBot..."

# create a virtual environment in ./venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip inside venv
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Done
echo "Setup complete!"
echo ""
echo "To run the bot, activate the environment first:"
echo "    source venv/bin/activate"
echo "Then run:"
echo "    python main.py"
echo ""
echo "To exit the environment later, run:"
echo "    deactivate"
