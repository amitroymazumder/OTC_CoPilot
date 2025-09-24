from core.retriever import RetrieverFactory
from core.sql_generator import generate_sql
from core.sql_validator import validate_sql
from core.db_connector import run_query

class Engine:
    """
    The main orchestrator for NL → SQL → Execution pipeline.
    """
    def __init__(self, backend="chroma"):
        # Initialize retriever (Chroma / Weaviate / Graph)
        self.retriever = RetrieverFactory(backend=backend)

    def ask(self, question: str):
        """
        Executes the full pipeline:
        - Retrieves context
        - Generates SQL
        - Validates SQL
        - Executes against MS SQL
        """
        # Step 1: Retrieve context (differs per backend)
        context = self.retriever.query(question)

        # Step 2: Generate SQL with LLM
        sql = generate_sql(question, context)

        # Step 3: Validate SQL
        if not validate_sql(sql):
            return {"error": "Unsafe or invalid SQL generated."}

        # Step 4: Execute SQL
        result = run_query(sql)

        return {"sql": sql, "result": result}
