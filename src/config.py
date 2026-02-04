import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Endee Database Settings
ENDEE_HOST = os.getenv("ENDEE_HOST", "http://localhost:8080")
ENDEE_API_KEY = os.getenv("ENDEE_API_KEY", None)
COLLECTION_NAME = "documind_production"
DIMENSION = 384  # Matches the all-MiniLM-L6-v2 output

# NLP Model Settings
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
BATCH_SIZE = 64