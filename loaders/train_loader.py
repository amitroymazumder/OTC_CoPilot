import os
import yaml
import argparse

# Loaders
from loaders import loader_chromadb, loader_weaviate, loader_graphdb

KNOWLEDGE_DIR = "./knowledge"

def load_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

def flatten_knowledge():
    """
    Flatten all YAML knowledge files into a list of text docs.
    Used for ChromaDB & Weaviate.
    """
    schema = load_yaml(os.path.join(KNOWLEDGE_DIR, "schema.yaml"))
    relationships = load_yaml(os.path.join(KNOWLEDGE_DIR, "relationships.yaml"))
    primary_keys = load_yaml(os.path.join(KNOWLEDGE_DIR, "primary_keys.yaml"))
    master_data = load_yaml(os.path.join(KNOWLEDGE_DIR, "master_data.yaml"))
    rules = load_yaml(os.path.join(KNOWLEDGE_DIR, "rules.yaml"))

    documents, ids = [], []

    # Schema
    for table in schema.get("tables", []):
        ids.append(f"table_{table['name']}")
        documents.append(
            f"Table {table['name']} with columns: "
            f"{', '.join([c['name'] for c in table['columns']])}"
        )

    # Relationships
    for rel in relationships.get("relationships", []):
        ids.append(f"rel_{rel['from_table']}_{rel['to_table']}")
        documents.append(
            f"FK: {rel['from_table']}.{rel['from_column']} -> "
            f"{rel['to_table']}.{rel['to_column']}"
        )

    # Primary Keys
    for pk in primary_keys.get("primary_keys", []):
        ids.append(f"pk_{pk['table']}_{pk['column']}")
        documents.append(f"Primary key on {pk['table']}: {pk['column']}")

    # Master Data
    for k, vals in master_data.items():
        ids.append(f"master_{k}")
        documents.append(f"Master {k} values: {', '.join(vals)}")

    # Rules
    for rule in rules.get("rules", []):
        ids.append(f"rule_{rule['name']}")
        documents.append(f"Rule: {rule['name']} - {rule['description']}")

    return documents, ids, schema, relationships, primary_keys, master_data, rules


def train_chroma():
    print("🔹 Loading into ChromaDB...")
    loader_chromadb.init()

def train_weaviate():
    print("🔹 Loading into Weaviate...")
    loader_weaviate.init()

def train_graph():
    print("🔹 Loading into Neo4j GraphDB...")
    loader_graphdb.init()


def train_all():
    print("📂 Flattening knowledge...")
    flatten_knowledge()  # ensures YAMLs exist / valid

    train_chroma()
    train_weaviate()
    train_graph()

    print("✅ Training complete: Knowledge loaded into ChromaDB, Weaviate, and GraphDB.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train OTC Copilot knowledge base")
    parser.add_argument(
        "--only",
        choices=["chroma", "weaviate", "graph", "all"],
        default="all",
        help="Choose which backend(s) to train (default: all)"
    )
    args = parser.parse_args()

    if args.only == "chroma":
        train_chroma()
    elif args.only == "weaviate":
        train_weaviate()
    elif args.only == "graph":
        train_graph()
    else:
        train_all()
