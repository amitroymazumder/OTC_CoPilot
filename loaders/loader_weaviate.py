import os
import yaml
import weaviate

KNOWLEDGE_DIR = "./knowledge"
WEAVIATE_URL = "http://localhost:8080"   # replace with your enterprise cluster endpoint

def load_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

def init():
    """
    Initializes Weaviate retriever.
    Loads YAML knowledge into Weaviate class `OTCKnowledge`.
    """
    client = weaviate.Client(WEAVIATE_URL)

    # Define schema if not exists
    class_name = "OTCKnowledge"
    if not client.schema.exists(class_name):
        client.schema.create_class({
            "class": class_name,
            "vectorizer": "text2vec-transformers"
        })

    # Load YAMLs
    schema = load_yaml(os.path.join(KNOWLEDGE_DIR, "schema.yaml"))
    relationships = load_yaml(os.path.join(KNOWLEDGE_DIR, "relationships.yaml"))
    primary_keys = load_yaml(os.path.join(KNOWLEDGE_DIR, "primary_keys.yaml"))
    master_data = load_yaml(os.path.join(KNOWLEDGE_DIR, "master_data.yaml"))
    rules = load_yaml(os.path.join(KNOWLEDGE_DIR, "rules.yaml"))

    def add_doc(text):
        client.data_object.create({"content": text}, class_name=class_name)

    # Flatten and add
    for table in schema["tables"]:
        add_doc(f"Table {table['name']} with columns: {', '.join([c['name'] for c in table['columns']])}")
    for rel in relationships["relationships"]:
        add_doc(f"FK: {rel['from_table']}.{rel['from_column']} -> {rel['to_table']}.{rel['to_column']}")
    for pk in primary_keys["primary_keys"]:
        add_doc(f"Primary key on {pk['table']}: {pk['column']}")
    for k, vals in master_data.items():
        add_doc(f"Master {k} values: {', '.join(vals)}")
    for rule in rules["rules"]:
        add_doc(f"Rule: {rule['name']} - {rule['description']}")

    class Retriever:
        def query(self, question, top_k=5):
            result = client.query.get("OTCKnowledge", ["content"]) \
                .with_near_text({"concepts": [question]}) \
                .with_limit(top_k).do()
            return [x["content"] for x in result["data"]["Get"]["OTCKnowledge"]]

    return Retriever()
