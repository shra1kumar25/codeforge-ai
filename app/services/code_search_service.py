from app.services.embedding_service import create_embedding
from app.vector_store.vector_store import VectorStore


class CodeSearchService:

    def __init__(self):
        self.store = VectorStore()

    def add_document(self, document: str):
        vector = create_embedding(document)
        self.store.add(vector, document)

    def search(self, query: str, top_k: int = 3):
        query_vector = create_embedding(query)

        return self.store.search(
            query_vector,
            top_k=top_k,
        )


code_search = CodeSearchService()
