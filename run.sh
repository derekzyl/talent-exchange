#!/bin/bash

set -e  # Exit on error

# Check for .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found."

    if [ -f "example.env" ]; then
        echo "📄 Found example.env, creating .env from it..."
        cp example.env .env
        echo "✅ .env file created."
    else
        echo "❌ example.env not found. Cannot continue without .env file."
        exit 1
    fi
fi

# Install pip if not installed
if ! command -v pip &> /dev/null; then
    echo "Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install pipenv if not installed
if ! command -v pipenv &> /dev/null; then
    echo "Installing pipenv..."
    pip install --user pipenv
    export PATH="$HOME/.local/bin:$PATH"
fi


# Add other dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements.txt..."
    pipenv run pip install -r requirements.txt
fi

# Run the FastAPI app
echo "Starting FastAPI server..."
pipenv run fastapi run
