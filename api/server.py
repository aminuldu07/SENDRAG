from fastapi import FastAPI
from sendrag.chat import generate_response

app = FastAPI()

@app.get("/query/")
def query_chatbot(question: str):
    answer = generate_response(question)
    return {"response": answer}
