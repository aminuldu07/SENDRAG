# import openai
# from sendrag.retrieval import retrieve_documents

# openai.api_key = "YOUR_OPENAI_API_KEY"

# def generate_response(query):
#     context = retrieve_documents(query)
#     prompt = f"Relevant documents:\n{context}\n\nUser query: {query}\nAnswer:"
#     response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
#     return response["choices"][0]["message"]["content"]

from sendrag.retrieval import retrieve_documents
import subprocess

def generate_response(query, model="llama3.2"):
    # Retrieve relevant documents for context
    context = retrieve_documents(query)

    # Combine context and query into prompt
    prompt = f"Relevant documents:\n{context}\n\nUser query: {query}\nAnswer:"

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running Ollama: {e.stderr}"
