#!/bin/bash

# Update system (Ubuntu)
sudo apt update -y && sudo apt upgrade -y

# Install Git
sudo apt install git -y

# Install Python 3 and pip
sudo apt install -y python3 python3-pip

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Clone frontend repo
git clone https://github.com/aminuldu07/SENDRAG.git

# Move to frontend directory
cd SENDRAG

# Install dependencies
poetry install

# Optional: Start the frontend server (Streamlit or Flask, depending on setup)
# Replace with actual command if different
poetry run streamlit run app.py --server.port 8501 --server.address 0.0.0.0
