# database.py
from qdrant_client import QdrantClient
from qdrant_client.http import models

class DatabaseHandler:
    def __init__(self, qdrant_host, qdrant_key):
        self.client = QdrantClient(url=qdrant_host, api_key=qdrant_key)
        self.collection_name = "xray_embeddings"  
        print('connected to QDrant')
        
    def search_by_text(self, text_embedding, limit=5):
        """
        Search the database by text embedding
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=text_embedding,
            limit=limit
        )
        return search_result
    
    def search_text_with_payload(self, text_embedding, limit=5):
        """
        Search for text embeddings in the payload
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=text_embedding,
            with_payload=True,
            limit=limit
        )
        return search_result