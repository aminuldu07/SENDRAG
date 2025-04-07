import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import chromadb
from sentence_transformers import SentenceTransformer

# Load OpenAI API key

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("documents")

def query_documents(question):
    """Retrieve relevant documents and answer using OpenAI GPT-4."""
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=3)

    # Combine retrieved text
    context = "\n".join(results["documents"][0]) if results["documents"] else "No relevant information found."

    prompt = f"""You are an AI assistant answering based on retrieved documents.
    Context: {context}
    Question: {question}
    Answer:"""

    response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "system", "content": "You are an expert assistant."},
              {"role": "user", "content": prompt}])

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    question = input("Ask a question: ")
    answer = query_documents(question)
    print("\nAnswer:", answer)
