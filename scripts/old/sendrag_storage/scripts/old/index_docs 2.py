from sendrag.embedder import get_embedding
from sendrag.vector_store import VectorStore
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def index_documents(folder_path):
    vector_db = VectorStore()
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            if filename.endswith(".txt"):
                with open(filepath, 'r') as f:
                    text = f.read().strip()
            elif filename.endswith(".pdf"):
                text = extract_text_from_pdf(filepath)
            else:
                print(f"Skipping unsupported file: {filename}")
                continue

            if text:
                embedding = get_embedding(text).cpu().numpy()
                vector_db.add_document(text, embedding)
    return vector_db

if __name__ == "__main__":
    folder = "data"
    db = index_documents(folder)
    # Test query
    query = "TS"
    query_emb = get_embedding(query).cpu().numpy()
    results = db.search(query_emb)
    print("Search results:", results)
