# server.py
#from sendrag.config import Config
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sendrag.sendrag_app import VectorStore, get_embedding, generate_response
import faiss
import pickle
import numpy as np


#print(Config.DEBUG)
#print(Config.OPENAI_API_KEY)

app = FastAPI()

# ---- Load vector store ----
EMBEDDING_DIM = 384  # for MiniLM model
FAISS_INDEX_PATH = "models/faiss_index.idx"
DOCUMENTS_PATH = "models/documents.pkl"

# Load FAISS index and corresponding documents
index = faiss.read_index(FAISS_INDEX_PATH)
with open(DOCUMENTS_PATH, "rb") as f:
    documents = pickle.load(f)

# Initialize VectorStore
vector_db = VectorStore(embedding_dim=EMBEDDING_DIM, index=index, documents=documents)

# ---- Utility functions ----

def convert_np_types(obj):
    """Convert numpy types to native Python types recursively."""
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, (list, tuple)):
        return [convert_np_types(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    return obj

def get_snippet(text, max_len=300):
    """Extract a short snippet from text (ending at a period if possible)."""
    snippet = text[:max_len]
    return snippet[:snippet.rfind('.') + 1] if '.' in snippet else snippet

# ---- API Endpoints ----

@app.post("/query")
async def query_docs(request: Request):
    """Accepts a JSON body with {'query': 'your question'} and returns the response."""
    body = await request.json()
    query = body.get("query")

    if not query:
        return JSONResponse(status_code=400, content={"error": "Missing 'query' in request body"})

    print(f"Received query: {query}")

    # Step 1: Get embedding
    embedding = get_embedding(query)

    # Step 2: Search relevant docs
    results = vector_db.search(embedding, top_k=3)
    
    print("🔍 Raw search results:")
    for i, doc in enumerate(results):
        print(f"Doc {i + 1}:\n{doc[:500]}\n{'-' * 40}")  # Print first 500 chars of each doc


    # Step 3: Build context and generate response
    context = "\n\n".join([get_snippet(doc) for doc in results])
    print("Context built from search results.")

    response = generate_response(query, context=context)

    return JSONResponse(content=convert_np_types({
        "query": query,
        "response": response
        #"sources": [get_snippet(doc) for doc in results],
    }))
