import streamlit as st
import os
import time
from src.endee_client import EndeeClient
from src.ingest import process_pdf, model
from src.config import ENDEE_HOST, ENDEE_API_KEY, COLLECTION_NAME, DIMENSION, DATA_DIR

# --- Init ---
st.set_page_config(page_title="DocuMind AI", layout="wide", page_icon="🧠")
client = EndeeClient(ENDEE_HOST, ENDEE_API_KEY)

# --- Header ---
st.title("🧠 DocuMind")
st.markdown(f"**Powered by [Endee](https://github.com/EndeeLabs/endee)** | High-Performance Vector Search")

# --- Status Indicator ---
if client.is_healthy():
    st.sidebar.success("🟢 Endee DB Connected")
else:
    st.sidebar.error("🔴 Endee DB Disconnected")
    st.sidebar.info("Run `docker-compose up -d`")

# --- Sidebar: Ingestion ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Ingest Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please select files first.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Ensure data dir exists
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)
            
            # Create Collection
            client.create_collection(COLLECTION_NAME, DIMENSION)
            
            total_chunks = 0
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Save locally
                file_path = os.path.join(DATA_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process & Vectorize
                vectors, ids, metas = process_pdf(file_path)
                
                if vectors:
                    client.insert_batch(COLLECTION_NAME, vectors, ids, metas)
                    total_chunks += len(vectors)
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("Done!")
            st.success(f"Successfully indexed {total_chunks} chunks!")

# --- Main: Search Interface ---
st.subheader("Semantic Search")
query = st.text_input("Ask a question about your documents:", placeholder="e.g., What are the safety compliance rules?")

if query:
    start_time = time.time()
    
    # 1. Embed Query
    query_vector = model.encode([query])[0].tolist()
    
    # 2. Search Endee
    results = client.search(COLLECTION_NAME, query_vector, top_k=4)
    duration = time.time() - start_time
    
    # 3. Render Results
    st.caption(f"Search completed in {duration:.3f}s")
    
    matches = results.get("matches", [])
    if matches:
        for match in matches:
            meta = match.get("metadata", {})
            score = match.get("score", 0.0)
            
            with st.expander(f"📄 {meta.get('source', 'Doc')} (Score: {score:.3f})", expanded=True):
                st.markdown(f"> {meta.get('text', '')}")
    else:
        st.info("No relevant matches found. Try ingesting some documents first.")