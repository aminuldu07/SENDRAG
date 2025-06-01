import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("documents")

def extract_text_from_pdfs(pdf_folder):
    """Extract text from PDFs in a folder."""
    documents = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file)
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                documents.append((file, text))
    return documents

def process_and_store_pdfs(pdf_folder):
    """Process PDFs and store embeddings in ChromaDB."""
    documents = extract_text_from_pdfs(pdf_folder)

    for filename, text in documents:
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]  # Chunking text
        embeddings = embed_model.encode(chunks).tolist()

        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[f"{filename}-{i}"],
                documents=[chunk],
                embeddings=[embeddings[i]]
            )

    print("PDFs processed and stored.")

if __name__ == "__main__":
    process_and_store_pdfs("pdfs/")
