from core.retriever import RetrieverFactory
from core.sql_generator import generate_sql
from core.sql_validator import validate_sql
from core.db_connector import run_query

class Engine:
    def __init__(self, backend="chroma"):
        self.retriever = RetrieverFactory(backend=backend)

    def ask(self, question: str):
        context = self.retriever.query(question)
        sql = generate_sql(question, context)
        if not validate_sql(sql):
            return {"error": "Unsafe SQL generated"}
        result = run_query(sql)
        return {"sql": sql, "result": result}
