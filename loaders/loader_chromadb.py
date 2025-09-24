import chromadb
from chromadb.utils import embedding_functions

def init():
    client = chromadb.Client()
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="./models/all-MiniLM-L6-v2"  # local path
    )
    collection = client.get_or_create_collection(
        name="otc_copilot", embedding_function=embedding_func
    )

    class Retriever:
        def query(self, question, top_k=5):
            results = collection.query(query_texts=[question], n_results=top_k)
            return results["documents"][0]

    return Retriever()
