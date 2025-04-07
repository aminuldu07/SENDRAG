import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_dim=384):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []

    def add_document(self, text, embedding):
        self.documents.append(text)
        self.index.add(np.array([embedding], dtype=np.float32))

    def search(self, query_embedding, top_k=5):
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), top_k)
        return [self.documents[i] for i in indices[0] if i < len(self.documents)]
