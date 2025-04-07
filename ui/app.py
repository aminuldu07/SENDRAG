import streamlit as st
import requests

st.title("SEND-RAG - A SEND Document Assistant")

query = st.text_input("Enter your question:")

if st.button("Ask"):
    response = requests.get("http://127.0.0.1:8000/query/", params={"question": query})
    st.write("### Answer:")
    st.write(response.json()["response"])
