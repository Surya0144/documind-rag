import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Endee Settings
ENDEE_HOST = os.getenv("ENDEE_HOST", "http://localhost:8080")
ENDEE_COLLECTION = "documind_production"
ENDEE_DIMENSION = 384  # Matches all-MiniLM-L6-v2

# Model Settings
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
BATCH_SIZE = 64  # Number of vectors to push at once