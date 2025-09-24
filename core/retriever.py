import yaml
from loaders import loader_chromadb, loader_weaviate, loader_graphdb

class RetrieverFactory:
    def __init__(self, backend="chroma"):
        self.backend = backend
        if backend == "chroma":
            self.retriever = loader_chromadb.init()
        elif backend == "weaviate":
            self.retriever = loader_weaviate.init()
        elif backend == "graph":
            self.retriever = loader_graphdb.init()
        else:
            raise ValueError("Unsupported retriever backend")

    def query(self, question: str, top_k: int = 5):
        return self.retriever.query(question, top_k=top_k)
