import os
import uuid
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from src.config import CHUNK_SIZE, MODEL_NAME

model = SentenceTransformer(MODEL_NAME)

def process_file(file_path):
    reader = PdfReader(file_path)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    chunks = []
    for i in range(0, len(text), CHUNK_SIZE):
        chunk_text = text[i:i + CHUNK_SIZE + 50]
        chunks.append({
            "id": str(uuid.uuid4()),
            "text": chunk_text,
            "source": os.path.basename(file_path)
        })
    
    if not chunks: return [], [], []
    
    vectors = model.encode([c["text"] for c in chunks]).tolist()
    ids = [c["id"] for c in chunks]
    return vectors, ids, chunks