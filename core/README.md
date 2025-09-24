---

# 📂 `core/` – OTC Ops Copilot Core Logic

The `core/` folder contains the **brains of OTC Ops Copilot**.
This is where natural language queries are turned into **SQL queries**, validated, executed against the MS SQL database, and visualized for the user.

---

## 📌 Files & Responsibilities

### 🔹 `engine.py`

* **Main orchestrator** for the full NL → SQL → Execution pipeline.
* Steps:

  1. Get **context** from retriever (`ChromaDB`, `Weaviate`, or `GraphDB`).
  2. Generate SQL with LLM (`sql_generator.py`).
  3. Validate SQL (`sql_validator.py`).
  4. Run SQL against MS SQL (`db_connector.py`).
  5. Return both the **SQL** and the **results**.

---

### 🔹 `retriever.py`

* Acts as a **factory** to select the retriever backend:

  * **ChromaDB** → lightweight, local embeddings DB.
  * **Weaviate** → enterprise vector DB, integrates with in-house LLM.
  * **Graph (Neo4j)** → schema-aware retrieval (best for complex joins).
* Exposes a single method:

  ```python
  query(question, top_k=5)
  ```
* Keeps the **UI/backend decoupled** from specific database technologies.

---

### 🔹 `sql_generator.py`

* Calls an **LLM** (your in-house model, or external for POC) to convert:

  ```
  (Natural Language Question + Retrieved Context) → SQL
  ```
* Example:

  ```python
  sql = generate_sql("Show confirmed trades today", context)
  ```
* Designed to work with:

  * Internal LLM API (`http://inhouse-llm/api/v1/generate`)
  * Or external fallback (e.g., Gemini, OpenAI) for demo purposes.

---

### 🔹 `sql_validator.py`

* Ensures **safety & correctness** of generated SQL:

  * Must start with `SELECT`.
  * No destructive operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.).
  * Basic structure check (ensures `FROM` exists).
* Prevents accidental data corruption.
* Returns `True/False` on validation.

---

### 🔹 `db_connector.py`

* Handles connection to **MS SQL Server** (read-only).
* Reads DB credentials from `config/db_config.yaml`.
* Provides:

  * `get_connection()` → opens DB connection.
  * `run_query(sql)` → executes a query and returns a Pandas DataFrame.

⚠️ **Read-only enforcement** is strongly recommended (DB user should not have write privileges).

---

### 🔹 `visualizer.py`

* Uses **Plotly** to generate visualizations.
* Logic:

  * If multiple numeric columns → `bar chart`.
  * If single numeric column → `histogram`.
* Returns a chart object that Streamlit can display.

---

## 📌 Flow of Control

1. User enters NL question in UI (`app/app.py`).
2. `engine.ask()` pipeline runs:

   * Retriever fetches **schema/rules context**.
   * LLM generates SQL.
   * SQL is validated.
   * Query executed in MS SQL.
   * Results + visualization returned.
3. UI shows **SQL + results table + charts**.

---

## 📌 Backend Selection

* **ChromaDB** → POC / local lightweight usage.
* **Weaviate** → Enterprise use, integrates with in-house LLM.
* **GraphDB (Neo4j)** → Handles **complex joins, relationships**, useful for OTC trade confirmation schema.

---

✅ In short:
The **`core/` folder = logic & intelligence layer**, separating user-facing UI (`app/`) from database + LLM interactions.

---
