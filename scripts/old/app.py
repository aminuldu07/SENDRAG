import streamlit as st
import requests

st.title("SEND-RAG - A SEND Document Assistant")

query = st.text_input("Enter your question:")

if st.button("Search") and query.strip():
    with st.spinner("Searching..."):
        try:
            response = requests.post("http://localhost:8000/query", json={"query": query})
            if response.status_code == 200:
                results = response.json().get("results", [])
                if results:
                    st.write("Answer:")
                    # Just show first snippet or one combined answer
                    st.write(results[0])
                else:
                    st.write("No answer found.")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")

            
# import streamlit as st
# import requests

# st.title("SEND-RAG - A SEND Document Assistant")

# query = st.text_input("Enter your question:")

# if st.button("Search") and query.strip():
#     with st.spinner("Searching..."):
#         try:
#             response = requests.post("http://localhost:8000/query", json={"query": query})
#             if response.status_code == 200:
#                 answer = response.json().get("answer", "")
#                 if answer:
#                     st.markdown("### Answer:")
#                     st.write(answer)
#                 else:
#                     st.warning("No answer found.")
#             else:
#                 st.error(f"Error from server: {response.status_code}")
#         except Exception as e:
#             st.error(f"Request failed: {e}")



