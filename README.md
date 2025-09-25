# OTC Ops Copilot 🚀

An AI-powered assistant for **OTC Trade Confirmation** ops teams.  
Transforms **natural language → SQL → reports → dashboards**.  

---

## 📌 Features
- Natural Language → SQL → MS SQL results.  
- Visualizations with **Plotly**.  
- Report scheduling + notifications (PDF, Excel, Email, Slack).  
- Flexible backends: **ChromaDB**, **Weaviate**, **GraphDB**.  
- Knowledge layer with schema, master data, business rules.  

---
📂 Project Structure
```
otc-ops-copilot/
│
├── app/                          # Streamlit frontend
│   ├── app.py                    # Main entrypoint for UI
│   ├── components/               # UI widgets
│   │   ├── query_input.py
│   │   ├── results_table.py
│   │   └── charts.py
│   └── pages/                    # Optional: dashboards, reports
│       ├── dashboards.py
│       └── reports.py
│
├── core/                         # Core logic
│   ├── __init__.py
│   ├── engine.py                 # Orchestrates NL→SQL pipeline
│   ├── retriever.py              # Wrapper for Chroma / Weaviate / Graph
│   ├── sql_generator.py          # Calls LLM (in-house or external)
│   ├── sql_validator.py          # Ensures SELECT-only
│   ├── db_connector.py           # MS SQL read-only connector
│   └── visualizer.py             # Plotly charts
│
├── loaders/                      # Knowledge loaders
│   ├── loader_chromadb.py
│   ├── loader_weaviate.py
│   └── loader_graphdb.py
│
├── knowledge/                    # YAMLs (auto-generated from CSVs)
│   ├── schema.yaml
│   ├── relationships.yaml
│   ├── primary_keys.yaml
│   ├── master_data.yaml
│   └── rules.yaml
│
├── services/                     # Extensions
│   ├── scheduler.py              # APScheduler jobs
│   ├── report_generator.py       # WeasyPrint/ReportLab for reports
│   └── notifier.py               # Email/Slack notifications
│
├── config/                       # Configurations
│   ├── chromadb_config.yaml
│   ├── weaviate_config.yaml
│   ├── graphdb_config.yaml
│   ├── db_config.yaml
│   └── llm_config.yaml
│
├── tests/                        # Unit tests
│   ├── test_sql_validator.py
│   ├── test_retriever.py
│   └── test_examples.py
│
├── requirements.txt
├── README.md
└── run.py                        # Main entry point to start backend + UI.
```
```

otc-ops-copilot/
├── app/           # Streamlit UI
├── core/          # Core NL → SQL pipeline
├── loaders/       # Knowledge loaders (Chroma, Weaviate, GraphDB)
├── services/      # Scheduler, reports, notifications
├── knowledge/     # Business glossary + rules
├── config/        # DB + LLM configs
├── tests/         # Unit tests
├── requirements.txt
├── run.py
└── README.md

````
---

## ⚙️ Setup
1. Clone repo:  
```bash
   
   git clone https://github.com/your-org/otc-ops-copilot.git
   cd otc-ops-copilot
```

2. Create virtual env + install deps:

   ```
   bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
   pip install -r requirements.txt
   ```
3. Configure DB + retriever in `config/*.yaml`.
4. Run:

   ```
   bash
   python run.py
   ```

---

## 📊 Backends

* **ChromaDB** → for local development.
* **Weaviate** → for enterprise LLM integration.
* **GraphDB (Neo4j)** → for schema reasoning.

Switch backend in `config/llm_config.yaml`:

```
yaml
provider: "weaviate"
```

---

## ✅ Roadmap

* Add support for settlement DB.
* Add fine-tuning with ops-provided SQL examples.
* Add RBAC (role-based access control) for sensitive data.

---

## 🛡️ Safety

* All DB connections are **read-only**.
* SQL validator enforces **SELECT-only queries**.
* Ops teams can trust no data will be modified.

```

---

✅ With this, your **entire project structure is now complete**:
- Each folder (`app`, `core`, `loaders`, `services`, `knowledge`, `config`, `tests`) has full code + documentation.  
- Root-level files (`requirements.txt`, `run.py`, `README.md`) make it easy to run & onboard new users.  
