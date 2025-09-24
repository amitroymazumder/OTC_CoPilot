from loaders import loader_chromadb, loader_weaviate, loader_graphdb

class RetrieverFactory:
    """
    Factory pattern to choose retriever backend.
    """
    def __init__(self, backend="chroma"):
        self.backend = backend

        if backend == "chroma":
            # ChromaDB retriever
            self.retriever = loader_chromadb.init()
        elif backend == "weaviate":
            # Weaviate retriever
            self.retriever = loader_weaviate.init()
        elif backend == "graph":
            # Graph (Neo4j) retriever
            self.retriever = loader_graphdb.init()
        else:
            raise ValueError("Unsupported retriever backend")

    def query(self, question: str, top_k: int = 5):
        """
        Retrieve context documents relevant to the question.
        """
        return self.retriever.query(question, top_k=top_k)
