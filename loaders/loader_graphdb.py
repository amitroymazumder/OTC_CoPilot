import os
import yaml
from neo4j import GraphDatabase

KNOWLEDGE_DIR = "./knowledge"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

def load_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

def init():
    """
    Initializes Graph RAG retriever using Neo4j.
    Loads schema, relationships, PKs, master data, and rules as graph nodes.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    schema = load_yaml(os.path.join(KNOWLEDGE_DIR, "schema.yaml"))
    relationships = load_yaml(os.path.join(KNOWLEDGE_DIR, "relationships.yaml"))
    primary_keys = load_yaml(os.path.join(KNOWLEDGE_DIR, "primary_keys.yaml"))
    master_data = load_yaml(os.path.join(KNOWLEDGE_DIR, "master_data.yaml"))
    rules = load_yaml(os.path.join(KNOWLEDGE_DIR, "rules.yaml"))

    # Load schema into Neo4j
    with driver.session() as session:
        for table in schema["tables"]:
            session.run("MERGE (t:Table {name:$name})", {"name": table["name"]})
            for col in table["columns"]:
                session.run("""
                    MERGE (c:Column {name:$cname, type:$ctype, nullable:$nullable})
                    MERGE (t:Table {name:$tname})
                    MERGE (t)-[:HAS_COLUMN]->(c)
                """, {
                    "cname": col["name"], "ctype": col["type"],
                    "nullable": col["is_nullable"], "tname": table["name"]
                })

        for rel in relationships["relationships"]:
            session.run("""
                MATCH (t1:Table {name:$from}), (t2:Table {name:$to})
                MERGE (t1)-[:FK {from_column:$fc, to_column:$tc}]->(t2)
            """, {
                "from": rel["from_table"], "to": rel["to_table"],
                "fc": rel["from_column"], "tc": rel["to_column"]
            })

        for pk in primary_keys["primary_keys"]:
            session.run("""
                MATCH (t:Table {name:$tname})
                MERGE (pk:PrimaryKey {column:$col})
                MERGE (t)-[:HAS_PK]->(pk)
            """, {"tname": pk["table"], "col": pk["column"]})

        for k, vals in master_data.items():
            for v in vals:
                session.run("MERGE (m:MasterData {category:$cat, value:$val})", {"cat": k, "val": v})

        for rule in rules["rules"]:
            session.run("MERGE (r:Rule {name:$name, description:$desc})", {"name": rule["name"], "desc": rule["description"]})

    class Retriever:
        def query(self, question, top_k=5):
            """
            Demo query: returns related schema elements for debugging.
            Later: can integrate with a Cypher-based retriever (Graph RAG).
            """
            with driver.session() as session:
                result = session.run("""
                    MATCH (t:Table)-[:HAS_COLUMN]->(c:Column)
                    RETURN t.name as table, c.name as column LIMIT $k
                """, {"k": top_k})
                return [f"{r['table']}.{r['column']}" for r in result]

    return Retriever()
