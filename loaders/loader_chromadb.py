import os
import yaml
import chromadb
from chromadb.utils import embedding_functions

KNOWLEDGE_DIR = "./knowledge"

def load_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

def init():
    """
    Initializes ChromaDB retriever.
    Loads schema, relationships, PKs, master data, and rules from YAML.
    """
    client = chromadb.Client()

    # Local model path (downloaded manually, not from HuggingFace hub)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="./models/all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="otc_copilot", embedding_function=embedding_func
    )

    # Load YAMLs
    schema = load_yaml(os.path.join(KNOWLEDGE_DIR, "schema.yaml"))
    relationships = load_yaml(os.path.join(KNOWLEDGE_DIR, "relationships.yaml"))
    primary_keys = load_yaml(os.path.join(KNOWLEDGE_DIR, "primary_keys.yaml"))
    master_data = load_yaml(os.path.join(KNOWLEDGE_DIR, "master_data.yaml"))
    rules = load_yaml(os.path.join(KNOWLEDGE_DIR, "rules.yaml"))

    # Flatten into text docs
    documents, ids = [], []

    for table in schema["tables"]:
        ids.append(f"table_{table['name']}")
        documents.append(f"Table {table['name']} with columns: {', '.join([c['name'] for c in table['columns']])}")

    for rel in relationships["relationships"]:
        ids.append(f"rel_{rel['from_table']}_{rel['to_table']}")
        documents.append(f"FK: {rel['from_table']}.{rel['from_column']} -> {rel['to_table']}.{rel['to_column']}")

    for pk in primary_keys["primary_keys"]:
        ids.append(f"pk_{pk['table']}_{pk['column']}")
        documents.append(f"Primary key on {pk['table']}: {pk['column']}")

    for k, vals in master_data.items():
        ids.append(f"master_{k}")
        documents.append(f"Master {k} values: {', '.join(vals)}")

    for rule in rules["rules"]:
        ids.append(f"rule_{rule['name']}")
        documents.append(f"Rule: {rule['name']} - {rule['description']}")

    # Insert docs into Chroma
    if documents:
        collection.add(ids=ids, documents=documents)

    class Retriever:
        def query(self, question, top_k=5):
            results = collection.query(query_texts=[question], n_results=top_k)
            return results["documents"][0]

    return Retriever()
