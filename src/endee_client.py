import requests

class EndeeClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.headers = {"Content-Type": "application/json"}

    def is_alive(self):
        try:
            return requests.get(f"{self.base_url}/health", timeout=2).status_code == 200
        except:
            return False

    def create_collection(self, name, dimension):
        payload = {"name": name, "dimension": dimension, "metric": "cosine", "engine": "hnsw"}
        try:
            requests.post(f"{self.base_url}/api/v1/collection/create", json=payload, headers=self.headers)
        except:
            pass # Ignore if exists

    def insert_batch(self, collection, vectors, ids, metadata):
        payload = {"collection": collection, "vectors": vectors, "ids": ids, "metadata": metadata}
        return requests.post(f"{self.base_url}/api/v1/insert", json=payload, headers=self.headers).json()

    def search(self, collection, vector, top_k=3):
        payload = {"collection": collection, "vector": vector, "top_k": top_k, "include_metadata": True}
        return requests.post(f"{self.base_url}/api/v1/search", json=payload, headers=self.headers).json()