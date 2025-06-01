from sendrag.embedder import get_embedding
from sendrag.vector_store import VectorStore

vector_db = VectorStore()

def retrieve_documents(query):
    #query_embedding = get_embedding(query).cpu().numpy()
    query_embedding = get_embedding(query)
    return vector_db.search(query_embedding)
