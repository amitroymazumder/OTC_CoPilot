from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

def init():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    class Retriever:
        def query(self, question, top_k=5):
            # For demo, use simple Cypher query to return schema context
            with driver.session() as session:
                result = session.run("MATCH (t:Table)-[:HAS_COLUMN]->(c:Column) RETURN t.name, c.name LIMIT $k", {"k": top_k})
                return [f"{r['t.name']}.{r['c.name']}" for r in result]

    return Retriever()
