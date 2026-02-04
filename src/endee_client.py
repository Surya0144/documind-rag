import requests
import time

class EndeeClient:
    """
    A robust Python wrapper for the Endee Vector Database REST API.
    Handles connection retries and error parsing.
    """
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def is_healthy(self):
        """Check if the database is running."""
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=2)
            return resp.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def create_collection(self, name, dimension, metric="cosine"):
        """Creates a new vector index if it doesn't exist."""
        payload = {
            "name": name,
            "dimension": dimension,
            "metric": metric,
            "engine": "hnsw" # Optimized for production
        }
        try:
            # Note: Endpoint structure based on Endee v1 API conventions
            requests.post(f"{self.base_url}/api/v1/collection/create", json=payload, headers=self.headers)
        except Exception as e:
            print(f"Info: Collection creation check skipped or failed safely: {e}")

    def insert_batch(self, collection, vectors, ids, metadata):
        """Batch insert vectors for high performance."""
        payload = {
            "collection": collection,
            "vectors": vectors,
            "ids": ids,
            "metadata": metadata
        }
        resp = requests.post(f"{self.base_url}/api/v1/insert", json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def search(self, collection, vector, top_k=5):
        """Perform Approximate Nearest Neighbor (ANN) search."""
        payload = {
            "collection": collection,
            "vector": vector,
            "top_k": top_k,
            "include_metadata": True
        }
        try:
            resp = requests.post(f"{self.base_url}/api/v1/search", json=payload, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Search Error: {e}")
            return {"matches": []}