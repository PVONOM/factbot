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

# --- Load API keys automatically ---
export NEWSAPI_KEY=9623df25bca74ee2aa2043729792bba5
export API_KEY=AIzaSyDP21Zk8lO3U_ais0_NUm3HLL7bjztCfkw
export CX=a31bb0e4bd68b4707

echo "API keys loaded into environment."

# Done
echo "Setup complete!"
echo ""
echo "To run the bot (with API keys already loaded), make sure the venv is active:"
echo "    source venv/bin/activate"
echo "Then run:"
echo "    python main.py"
echo ""
echo "To exit the environment later, run:"
echo "    deactivate"
