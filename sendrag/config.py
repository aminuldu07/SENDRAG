# import os
# from dotenv import load_dotenv

# # Load from .env at the project root
# load_dotenv()

# class Config:
#     APP_ENV = os.getenv("APP_ENV", "production")
#     DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
#     PORT = int(os.getenv("PORT", 8000))

#     # Model and index paths
#     VECTOR_INDEX_PATH = os.getenv("VECTOR_INDEX_PATH", "models/faiss_index.idx")
#     DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "models/documents.pkl")

#     # API Keys
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# sendrag/config.py
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

LLAMA_MODEL_NAME = os.getenv("LLAMA_MODEL_NAME", "llama3.2")
EMBEDDER_MODEL_NAME = os.getenv("EMBEDDER_MODEL_NAME", "all-MiniLM-L6-v2")
