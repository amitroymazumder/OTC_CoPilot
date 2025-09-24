import weaviate

WEAVIATE_URL = "http://localhost:8080"

def init():
    client = weaviate.Client(WEAVIATE_URL)

    class Retriever:
        def query(self, question, top_k=5):
            result = client.query.get("OTCKnowledge", ["content"]) \
                .with_near_text({"concepts": [question]}) \
                .with_limit(top_k).do()
            return [x["content"] for x in result["data"]["Get"]["OTCKnowledge"]]

    return Retriever()
