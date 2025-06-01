# # app.py
import streamlit as st
import requests

st.set_page_config(page_title="SEND-RAG Assistant", layout="centered")
st.title("🧠 SEND-RAG - A SEND Document Assistant")

# User input
query = st.text_input("🔍 Enter your question:", placeholder="e.g., What is the TS parameter in SEND?")

# When button is clicked
if st.button("Search") and query.strip():
    with st.spinner("Searching through SEND documents..."):
        try:
            response = requests.post("http://localhost:8000/query", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                sources = data.get("sources", [])

                if response_text:
                    st.success("✅ Answer found:")
                    st.markdown(f"**Answer:** {response_text}")
                    st.markdown("---")
                    for i, source in enumerate(sources[:3], 1):  # Show top 3 sources
                        st.markdown(f"**Source {i}:**")
                        st.write(source)
                        st.markdown("---")
                else:
                    st.warning("😕 No relevant answer found.")
            else:
                st.error(f"🚫 Server error: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")








# import streamlit as st
# import requests

# st.set_page_config(page_title="SEND-RAG Assistant", layout="centered")
# st.title("🧠 SEND-RAG - A SEND Document Assistant")

# # User input
# query = st.text_input("🔍 Enter your question:", placeholder="e.g., What is the TS parameter in SEND?")

# # When button is clicked
# if st.button("Search") and query.strip():
#     with st.spinner("Searching through SEND documents..."):
#         try:
#             response = requests.post("http://localhost:8000/query", json={"query": query})
#             if response.status_code == 200:
#                 data = response.json()
#                 results = data.get("results", [])

#                 if results:
#                     st.success("✅ Answer found:")
#                     for i, result in enumerate(results[:3], 1):  # show top 3 results
#                         st.markdown(f"**Result {i}:**")
#                         st.write(result)
#                         st.markdown("---")
#                 else:
#                     st.warning("😕 No relevant answer found.")
#             else:
#                 st.error(f"🚫 Server error: {response.status_code}")
#         except Exception as e:
#             st.error(f"⚠️ Request failed: {e}")
