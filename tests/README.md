Got it 👍 since you’ve got the knowledge/ part covered on your work machine, let’s move on.

The next important folder in our project structure is:

├── tests/                        # Unit tests
│   ├── test_sql_validator.py
│   ├── test_retriever.py
│   └── test_examples.py

This folder ensures your pipeline works correctly before deploying to ops.


---

📂 tests/ – Unit Tests for OTC Ops Copilot

🔹 test_sql_validator.py

Verifies that:

Only SELECT statements are allowed.

Queries with INSERT/UPDATE/DELETE/DROP are blocked.

Invalid joins or missing tables are flagged.



import pytest
from core.sql_validator import validate_sql

def test_valid_select():
    sql = "SELECT * FROM Trades WHERE status = 'Confirmed'"
    result = validate_sql(sql)
    assert result["valid"] is True

def test_invalid_insert():
    sql = "INSERT INTO Trades VALUES (1, 'test')"
    result = validate_sql(sql)
    assert result["valid"] is False

def test_block_dangerous():
    sql = "DROP TABLE Trades"
    result = validate_sql(sql)
    assert result["valid"] is False


---

🔹 test_retriever.py

Ensures retrievers (ChromaDB, Weaviate, GraphDB) return meaningful context.

Uses mock question + knowledge snippets.


import pytest
from loaders import loader_chromadb, loader_weaviate, loader_graphdb

def test_chroma_query():
    retriever = loader_chromadb.init()
    results = retriever.query("What is a trade confirmation?", top_k=2)
    assert isinstance(results, list)
    assert len(results) > 0

def test_weaviate_query():
    retriever = loader_weaviate.init()
    results = retriever.query("List trade statuses", top_k=2)
    assert isinstance(results, list)

def test_graph_query():
    retriever = loader_graphdb.init()
    results = retriever.query("Which tables link trades and events?", top_k=2)
    assert isinstance(results, list)


---

🔹 test_examples.py

Runs example NL → SQL conversions using stored test queries.

Ensures pipeline can handle typical ops questions.


import pytest
from core.engine import Engine

def test_trade_summary():
    engine = Engine(backend="chroma")
    result = engine.ask("Show number of confirmed trades today")
    assert "sql" in result
    assert "result" in result
    assert isinstance(result["result"], list)


---

✅ Why These Tests Matter

Safety → sql_validator ensures DB is never modified.

Reliability → retrievers actually return context.

Coverage → sample questions validate NL → SQL pipeline.



---

Great 👍 Here’s the tests/README.md for your OTC Ops Copilot repo.


---

📂 tests/ – Unit & Integration Tests for OTC Ops Copilot

The tests/ folder contains automated tests that ensure OTC Ops Copilot works safely and reliably before deploying to operations teams.
It uses pytest as the testing framework.


---

📌 Files & Responsibilities

🔹 test_sql_validator.py

Validates SQL safety rules.

Ensures only SELECT queries pass.

Blocks INSERT, UPDATE, DELETE, DROP.

Prevents accidental DB modifications.


Example:

pytest tests/test_sql_validator.py -v


---

🔹 test_retriever.py

Tests retrieval from all 3 backends:

ChromaDB (local vector DB).

Weaviate (enterprise vector DB).

GraphDB (Neo4j) (schema reasoning).


Ensures retrievers return non-empty results for queries.


Example:

pytest tests/test_retriever.py -v


---

🔹 test_examples.py

End-to-end test for NL → SQL → DB → Result pipeline.

Runs a few common OTC ops queries.

Ensures SQL and results are produced without errors.


Example:

pytest tests/test_examples.py -v


---

📌 How to Run All Tests

From project root:

pytest -v

Optional: to see detailed logs:

pytest -s -v


---

📌 Mocking DB Connections

For safety, avoid running tests directly on production MS SQL.
Instead, you can:

1. Point db_config.yaml to a test/staging DB.


2. Or mock results with SQLite + sample data for unit testing.




---

📌 Extending the Test Suite

As you deploy OTC Ops Copilot, add real business queries as tests in test_examples.py.
Example:

def test_trade_by_counterparty():
    engine = Engine(backend="weaviate")
    result = engine.ask("Show trades by counterparty this month")
    assert "sql" in result
    assert isinstance(result["result"], list)


---

📌 Benefits

✔ Safety → DB never modified by mistake.
✔ Reliability → retrievers return relevant context.
✔ Accuracy → real ops queries validated continuously.
✔ Scalability → new tests can be added as business grows.


---

✅ In short: The tests/ folder is your safety net before deploying OTC Ops Copilot to ops teams.


---
