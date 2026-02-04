import streamlit as st
import os
from src.endee_client import EndeeClient
from src.ingest import process_file, model
from src.config import ENDEE_HOST, COLLECTION_NAME, DIMENSION, DATA_DIR

client = EndeeClient(ENDEE_HOST)
st.set_page_config(page_title="DocuMind", layout="wide")

st.title("🧠 DocuMind: Endee Vector Search")

# Sidebar: Ingestion
with st.sidebar:
    st.header("📂 Upload Data")
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("Ingest"):
        if not files: st.warning("No files selected.")
        else:
            if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
            client.create_collection(COLLECTION_NAME, DIMENSION)
            
            total_chunks = 0
            for uploaded_file in files:
                path = os.path.join(DATA_DIR, uploaded_file.name)
                with open(path, "wb") as f: f.write(uploaded_file.getbuffer())
                
                vecs, ids, metas = process_file(path)
                if vecs:
                    client.insert_batch(COLLECTION_NAME, vecs, ids, metas)
                    total_chunks += len(vecs)
            st.success(f"Indexed {total_chunks} chunks!")

# Main: Search
query = st.text_input("Ask a question about your documents:")
if query:
    q_vec = model.encode([query])[0].tolist()
    res = client.search(COLLECTION_NAME, q_vec)
    
    matches = res.get("matches", [])
    if matches:
        for m in matches:
            with st.expander(f"Source: {m['metadata']['source']} (Score: {m['score']:.2f})", expanded=True):
                st.markdown(m['metadata']['text'])
    else:
        st.info("No matches found.")