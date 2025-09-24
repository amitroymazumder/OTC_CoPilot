---

# 📂 `app/` – OTC Ops Copilot UI Layer

The `app/` folder contains the **Streamlit-based frontend** for OTC Ops Copilot.
This is the part that operations users interact with — asking questions in **natural language**, viewing the generated **SQL queries**, and exploring **results + visualizations**.

---

## 📌 Files & Responsibilities

### 🔹 `app.py`

* **Main entrypoint** for the Streamlit app.
* Handles:

  * UI layout (title, sidebar, query input).
  * Lets the user **select retriever backend** (`ChromaDB`, `Weaviate`, `GraphDB`).
  * Passes the natural language question → `core/engine.py`.
  * Displays:

    * Generated **SQL**
    * **Result table**
    * **Plotly chart**

---

### 🔹 `components/`

Reusable UI widgets:

* **`query_input.py`**
  Provides a text box for user’s **natural language query**.

* **`results_table.py`**
  Displays query results in a **Streamlit dataframe**.
  Supports both pandas DataFrames and list-of-dicts.

* **`charts.py`**
  Uses **Plotly** to show simple visualizations from query results.
  Auto-detects numeric columns for charts.

---

### 🔹 `pages/`

Optional Streamlit **multi-page apps**:

* **`dashboards.py`**
  Contains **pre-built dashboards** (e.g., confirmed trades per day).
  Useful for recurring analytics beyond ad-hoc queries.

* **`reports.py`**
  Lets users **schedule reports** (daily/weekly).
  Integrates with `services/scheduler.py` and `services/report_generator.py`.

---

## 📌 Flow of Control

1. User enters a **question** in `query_input`.
2. `app.py` calls the **engine** (`core/engine.py`) → runs NL→SQL pipeline.
3. Generated SQL is validated, executed (read-only), and results returned.
4. Results are shown in:

   * **Table** (`results_table`)
   * **Chart** (`charts`)
5. If using `pages/`, dashboards and scheduled reports are also available.

---

## 📌 Backend Selection

* The app lets the user **switch retriever backend** at runtime:

  * `chroma` → lightweight, local vector store.
  * `weaviate` → enterprise vector DB, integrates with in-house LLM.
  * `graph` → schema-aware retrieval (Neo4j).

All backend-specific logic is abstracted inside `core/retriever.py` —
so the UI remains the same regardless of backend.

---

✅ In short:
The **`app/` folder = UI/UX layer**, while all intelligence (NL→SQL, retrieval, validation, DB connection) happens in the **`core/` layer**.

---
