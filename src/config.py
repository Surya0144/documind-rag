import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Settings
ENDEE_HOST = os.getenv("ENDEE_HOST", "http://localhost:8080")
COLLECTION_NAME = "documind_kb"
MODEL_NAME = "all-MiniLM-L6-v2"
DIMENSION = 384
CHUNK_SIZE = 500