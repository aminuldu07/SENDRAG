# #!/bin/bash

# # Activate poetry virtual environment
# source /Users/amin/Library/Caches/pypoetry/virtualenvs/sendrag-*/bin/activate

# echo "Starting frontend..."
# streamlit run ui/app.py
#!/bin/bash

# Activate poetry environment
source /Users/amin/Library/Caches/pypoetry/virtualenvs/sendrag-s8hi-jRC-py3.13/bin/activate

# Add current project to PYTHONPATH
export PYTHONPATH=$(pwd)

# Run the frontend app
poetry run streamlit run ui/app.py
