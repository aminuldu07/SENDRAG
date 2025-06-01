import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def normalize(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

class VectorStore:
    def __init__(self, embedding_dim, index=None, documents=None):
        self.embedding_dim = embedding_dim
        if index is None:
            self.index = faiss.IndexFlatL2(embedding_dim)
        else:
            self.index = index
        
        if documents is None:
            self.documents = []
        else:
            self.documents = documents

    def add_document(self, doc_text, embedding):
        norm_emb = normalize(embedding).astype('float32')
        self.documents.append(doc_text)
        self.index.add(np.array([norm_emb]))

    def search(self, query_embedding, top_k=5):
        if self.index.ntotal == 0:
            return []
        norm_query = normalize(query_embedding).astype('float32')
        D, I = self.index.search(np.array([norm_query]), top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx == -1 or idx >= len(self.documents):
                continue
            results.append((self.documents[idx], dist))
        return results


if __name__ == "__main__":
    # Initialize model and VectorStore
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_dim = 384  # for all-MiniLM-L6-v2

    store = VectorStore(embedding_dim)

    # Sample documents
    docs = [
        "This document talks about SEND standards.",
        "This document describes machine learning.",
        "Another text about data science and AI."
    ]

    # Add documents
    for doc in docs:
        emb = model.encode(doc)
        store.add_document(doc, emb)

    # Query
    query = "What is SEND?"
    query_emb = model.encode(query)

    # Search
    results = store.search(query_emb)

    print("Search Results:")
    for doc, dist in results:
        print(f"Distance: {dist:.4f} Document: {doc}")





# import faiss
# import numpy as np

# class VectorStore:
#     def __init__(self, embedding_dim, index=None, documents=None):
#         self.embedding_dim = embedding_dim
#         if index is None:
#             self.index = faiss.IndexFlatL2(embedding_dim)
#         else:
#             self.index = index
        
#         if documents is None:
#             self.documents = []
#         else:
#             self.documents = documents

#     def add_document(self, doc_text, embedding):
#         self.documents.append(doc_text)
#         self.index.add(np.array([embedding]).astype('float32'))

#     def search(self, query_embedding, top_k=5):
#         if self.index.ntotal == 0:
#             return []
#         D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
#         valid_indices = [i for i in I[0] if i != -1 and i < len(self.documents)]
#         return [self.documents[i] for i in valid_indices]



# import faiss
# import numpy as np

# class VectorStore:
#     def __init__(self, embedding_dim=384):
#         self.index = faiss.IndexFlatL2(embedding_dim)
#         self.documents = []

#     def add_document(self, text, embedding):
#         # embedding must be 1D numpy float32 array of length embedding_dim
#         if not isinstance(embedding, np.ndarray):
#             embedding = np.array(embedding, dtype=np.float32)
#         else:
#             embedding = embedding.astype(np.float32)
        
#         if embedding.ndim != 1 or embedding.shape[0] != self.index.d:
#             raise ValueError(f"Embedding must be 1D with length {self.index.d}")
        
#         self.documents.append(text)
#         # Add embedding as 2D array (num_vectors=1, dim)
#         self.index.add(embedding.reshape(1, -1))

#     def search(self, query_embedding, top_k=5):
#         if not isinstance(query_embedding, np.ndarray):
#             query_embedding = np.array(query_embedding, dtype=np.float32)
#         else:
#             query_embedding = query_embedding.astype(np.float32)
        
#         # Ensure query_embedding shape is (1, embedding_dim)
#         if query_embedding.ndim == 1:
#             query_embedding = query_embedding.reshape(1, -1)
#         elif query_embedding.ndim != 2 or query_embedding.shape[1] != self.index.d:
#             raise ValueError(f"Query embedding must be shape (1, {self.index.d})")
        
#         distances, indices = self.index.search(query_embedding, top_k)
        
#         print(f"Indices returned by FAISS: {indices}")
#         print(f"Documents stored: {len(self.documents)}")
#         print(f"FAISS index total vectors: {self.index.ntotal}")
        
#         # Filter out invalid indices (-1 or out-of-range)
#         valid_indices = []
#         for idx in indices[0]:
#             if idx == -1:
#                 # No more neighbors
#                 continue
#             if idx >= len(self.documents):
#                 print(f"Warning: FAISS returned index {idx} which is out of documents range")
#                 continue
#             valid_indices.append(idx)
        
#         # Return the corresponding documents
#         return [self.documents[i] for i in valid_indices]

#     def sanity_check(self):
#         print(f"Documents count: {len(self.documents)}")
#         print(f"FAISS index count: {self.index.ntotal}")
#         if len(self.documents) != self.index.ntotal:
#             raise RuntimeError("Mismatch between documents and FAISS index vectors!")

