import requests
import time
from typing import List, Dict, Optional, Any

class EndeeClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def _request(self, method: str, endpoint: str, payload: Dict = None) -> Dict:
        """Internal wrapper with error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            resp = self.session.request(method, url, json=payload, headers=self.headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ [Endee API Error] {e}")
            if resp is not None:
                print(f"   Server Response: {resp.text}")
            return {}

    def health_check(self) -> bool:
        """Verifies DB connection."""
        try:
            # Endee typically exposes a root or health endpoint
            resp = self.session.get(f"{self.base_url}/health", timeout=2)
            return resp.status_code == 200
        except:
            return False

    def create_collection(self, name: str, dimension: int, metric: str = "cosine"):
        """Creates a collection if it doesn't exist."""
        payload = {
            "name": name,
            "dimension": dimension,
            "metric": metric,
            "engine": "hnsw" # Explicitly requesting HNSW index
        }
        # Checking existence is implied in idempotent creation or error handling
        return self._request("POST", "/api/v1/collection/create", payload)

    def insert_batch(self, collection: str, vectors: List[List[float]], ids: List[str], metadata: List[Dict]):
        """Batch insert for high performance."""
        payload = {
            "collection": collection,
            "vectors": vectors,
            "ids": ids,
            "metadata": metadata
        }
        return self._request("POST", "/api/v1/insert", payload)

    def search(self, collection: str, vector: List[float], top_k: int = 5) -> Dict:
        """Performs ANN search."""
        payload = {
            "collection": collection,
            "vector": vector,
            "top_k": top_k,
            "include_metadata": True
        }
        return self._request("POST", "/api/v1/search", payload)