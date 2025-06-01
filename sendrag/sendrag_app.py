import os
import subprocess
import PyPDF2
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss  # assuming you’re using faiss
import numpy as np

# 1. Embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text, convert_to_tensor=False)

# 2. Text extraction functions
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_string()

def extract_text_from_folder(folder_path):
    text_data = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".pdf"):
            text_data.append(extract_text_from_pdf(file_path))
        elif file.endswith(".csv"):
            text_data.append(extract_text_from_csv(file_path))
    return text_data

# normalize function
def normalize(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

# 3. Simple in-memory vector store using FAISS
class VectorStore:
    def __init__(self, embedding_dim=384, index=None, documents=None):
        self.embedding_dim = embedding_dim
        self.index = index if index is not None else faiss.IndexFlatL2(embedding_dim)
        self.documents = documents if documents is not None else []

    def add_document(self, doc_text, embedding):
        norm_emb = normalize(embedding).astype('float32')
        self.documents.append(doc_text)
        self.index.add(np.array([norm_emb]))

    def search(self, embedding, top_k=3):
        emb_np = np.array([embedding]).astype("float32")
        D, I = self.index.search(emb_np, top_k)
        return [self.documents[i] for i in I[0]]


# 4. Initialize vector DB and load documents (👇 Add it here!)
vector_db = VectorStore(embedding_dim=384)
docs = extract_text_from_folder("data")  # Make sure 'data' folder exists
for text in docs:
    if text:
        embedding = get_embedding(text)
        vector_db.add_document(text, embedding)

# 5. Document retrieval
def retrieve_documents(query, top_k=3):
    query_embedding = get_embedding(query)
    return "\n---\n".join(vector_db.search(query_embedding, top_k=top_k))

def generate_prompt(query, context):
    return f"""You are a helpful assistant.

The user asked: "{query}"

Use the context below if it's helpful:
{context}

If the query matches the context or there's no specific question to answer, respond simply with the relevant content.
Otherwise, answer the query concisely based on the context.
"""

def generate_response(query, context=None, model="llama3.2"):
    if context is None:
        context = retrieve_documents(query)
    
    prompt = generate_prompt(query, context)  # Use your helper here

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating response: {e.stderr}"


# 7. CLI usage
if __name__ == "__main__":
    while True:
        query = input("Enter your question: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = generate_response(query)
        print("\nAnswer:\n", answer)
