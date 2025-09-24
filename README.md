# OTC_CoPilot
OTC_CoPilot

full OTC Ops Copilot project skeleton that supports all 3 backends:
ChromaDB (local RAG, lightweight POC).
Weaviate (enterprise, integrates with your in-house LLM).
Graph RAG (Neo4j, for schema-aware reasoning).

📂 Project Structure

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
└── run.py                        # Launch backend + UI
