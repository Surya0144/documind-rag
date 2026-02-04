import os
import uuid
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from src.config import CHUNK_SIZE, MODEL_NAME

# Load model once at module level for efficiency
print("Loading Embedding Model...")
model = SentenceTransformer(MODEL_NAME)

def process_pdf(file_path):
    """
    Parses a PDF and returns vectors, ids, and metadata.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        
        if not text.strip():
            return [], [], []

        # Chunking Strategy: Simple sliding window
        chunks = []
        for i in range(0, len(text), CHUNK_SIZE):
            chunk_text = text[i:i + CHUNK_SIZE + 50] # +50 char overlap
            chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk_text,
                "source": os.path.basename(file_path)
            })
        
        # Generate Embeddings
        texts = [c["text"] for c in chunks]
        vectors = model.encode(texts).tolist()
        ids = [c["id"] for c in chunks]
        
        return vectors, ids, chunks

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return [], [], []   