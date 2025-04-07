import openai
from sendrag.retrieval import retrieve_documents

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(query):
    context = retrieve_documents(query)
    prompt = f"Relevant documents:\n{context}\n\nUser query: {query}\nAnswer:"
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]
