# server.py
import faiss
import pickle
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sendrag.vector_store import VectorStore
from sendrag.embedder import get_embedding

from sendrag.chat import generate_response  # your function that calls Ollama

app = FastAPI()

# Load FAISS index and documents once at startup
index = faiss.read_index("faiss_index.idx")
with open("documents.pkl", "rb") as f:
    documents = pickle.load(f)

vector_db = VectorStore(embedding_dim=384, index=index, documents=documents)


def convert_np_types(obj):
    """
    Recursively convert numpy data types to native Python types for JSON serialization.
    """
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
    snippet = text[:max_len]
    if '.' in snippet:
        snippet = snippet[:snippet.rfind('.')+1]
    return snippet

@app.post("/query")
async def query_docs(request: Request):
    """
    Accepts a JSON body with {"query": "your question"} and returns relevant documents.
    """
    body = await request.json()
    query = body.get("query")
    if not query:
        return JSONResponse(status_code=400, content={"error": "Missing 'query' in request body"})

    print("Received query:", query)
    embedding = get_embedding(query)
    print("Received query:", query)
    results = vector_db.search(embedding, top_k=5)
    print("Search done")
    #Generate final answer using your RAG + Ollama approach
    answer = generate_response(query)
    return {"results": convert_np_types(results)}

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse

# app = FastAPI()

# def get_embedding(text):
#     # Your embedding code here
#     return [0.1, 0.2, 0.3]  # Dummy example

# def convert_np_types(results):
#     # Convert numpy types to Python types if needed
#     return results

# def get_snippet(text, max_len=300):
#     snippet = text[:max_len]
#     # Cut off at last period for full sentence
#     last_period = snippet.rfind('.')
#     if last_period != -1:
#         snippet = snippet[:last_period+1]
#     return snippet

# @app.post("/query")
# async def query_docs(request: Request):
#     body = await request.json()
#     query = body.get("query")
#     if not query:
#         return JSONResponse(status_code=400, content={"error": "Missing 'query' in request body"})

#     embedding = get_embedding(query)
#     results = vector_db.search(embedding, top_k=5)  # Your actual search

#     # Assume results is a list of strings (documents)
#     short_results = [get_snippet(doc) for doc in results]

#     # Combine all snippets into one answer (optional)
#     answer = " ".join(short_results)
#     return {"answer": answer}
