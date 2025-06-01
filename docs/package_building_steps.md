1. open gitbash
2. cd to ~?SEND-RAG
3. poetry init
4. Create folders and files using Git Bash:
5. mkdir sendrag api ui tests
6. touch sendrag/__init__.py
7. touch sendrag/data_loader.py sendrag/embedder.py sendrag/vector_store.py sendrag/retrieval.py sendrag/chat.py
8. touch api/server.py
9. touch ui/app.py
10. touch README.md
11. poetry install
12. paste all the codes in .py files
13. poetry add fastapi uvicorn streamlit faiss-cpu sentence-transformers PyPDF2 openai
14. poetry add transformers faiss-cpu torch flask numpy scikit-learn #  runtime dependencies (i.e., packages your app needs to function)
15. poetry add --group dev black pytest mypy flake8 # This adds development tools only used during coding/testing, not in production
16. poetry run uvicorn api.server:app --reload ( here got errors)............

17. need to install a package using pip 

## poetry shell (This will open a new shell session where the virtual environment is active)
pip install transformers==4.49.0
pip install accelerate==1.6.0

18. poetry run uvicorn api.server:app --reload (in terminal)
------------ streamlit run ui/app.py


## at mac##

brew install poetry ( from global directory)
# check the package structur by """ tree -L 2" from sendrag directory 
  ---------- tree -L 2"
  ----------- head -n 10 ui/app.py

# at Sendrag directory 
    --- poetry install 
    --- poetry env info --path (Check where the Poetry-managed environment lives: )
    ---  source /Users/amin/Library/Caches/pypoetry/virtualenvs/sendrag-s8hi-jRC-py3.13/bin/activate (activate poetry virtualenvs)
    --- which python ( python directory for the virtualenvs)
  
  
 #AWS--------------------------------------------------------------
    -- A1K2IAZVDON25TE3D3VINB14

SENDRAG/
│
├── sendrag/              # Core logic
│   ├── __init__.py
│   └── app.py            # Core functions/classes
│
├── api/                  # REST API (FastAPI or Flask)
│   └── server.py
│
├── ui/                   # Frontend (Streamlit, Gradio, etc.)
│   └── app.py
│
├── scripts/              # Dev and deployment scripts
│   └── build.py
│
├── data/                 # Static resources (can move to S3 in production)
│
├── models/               # faiss_index.idx, documents.pkl (modularize)
│
├── tests/                # Unit & integration tests
│   └── test_app.py
│
├── pyproject.toml        # Poetry-managed dependencies
├── run_app.py            # Entrypoint script
├── Dockerfile            # For containerizing the app
└── README.md


