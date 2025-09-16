#!/bin/bash

# Navigate to the agent directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the agent
uv run python main.py