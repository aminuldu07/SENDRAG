from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    #return model.encode(text, convert_to_tensor=True).cpu().numpy()
    return model.encode(text, convert_to_tensor=False)
