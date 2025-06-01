import sys
import os

# Add the parent directory to sys.path so Python can find embedder and vector_store modules
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pickle
import faiss
from sendrag.embedder import get_embedding
from sendrag.vector_store import VectorStore
from PyPDF2 import PdfReader

DATA_FOLDER = "./data"  # your folder with txt and pdf files

def load_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            text = load_text_from_txt(file_path)
            documents.append(text)
        elif filename.endswith(".pdf"):
            text = load_text_from_pdf(file_path)
            documents.append(text)
        else:
            print(f"Skipping unsupported file type: {filename}")
    return documents

def main():
    vector_db = VectorStore(embedding_dim=384)

    # Load documents from data folder
    docs = load_documents(DATA_FOLDER)
    print(f"Loaded {len(docs)} documents")

    # Add docs with embeddings to vector store
    for doc in docs:
        emb = get_embedding(doc)  # Make sure this returns a numpy array, no .cpu() calls here
        vector_db.add_document(doc, emb)

    print(f"FAISS index total vectors: {vector_db.index.ntotal}")
    print(f"Documents stored: {len(vector_db.documents)}")

    # Save the FAISS index
    faiss.write_index(vector_db.index, "faiss_index.idx")

    # Save documents list (pickle)
    with open("documents.pkl", "wb") as f:
        pickle.dump(vector_db.documents, f)

if __name__ == "__main__":
    main()
