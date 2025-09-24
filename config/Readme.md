Perfect 👍 Amit, now let’s cover the config/ folder.
This is where all the environment and backend configuration lives — so your ops/dev team can tune things without touching code.


---

📂 config/ – Configuration Files for OTC Ops Copilot

The config/ folder centralizes database, LLM, and retriever settings.
These files are in YAML format, making them easy to read, version, and update.


---

🔹 chromadb_config.yaml

# ChromaDB Configuration
persist_directory: "./chroma_store"
collection_name: "otc_copilot"
embedding_model: "./models/all-MiniLM-L6-v2"

# Query settings
top_k: 5

📌 Notes:

persist_directory → local folder where ChromaDB stores embeddings.

embedding_model → path to local SentenceTransformer model (since huggingface is blocked in office).

top_k → how many docs to retrieve per query.



---

🔹 db_config.yaml

# MS SQL Database Configuration
driver: "ODBC Driver 17 for SQL Server"
server: "your-sql-server.company.com"
port: 1433
database: "OTC_Trade_Confirmation"
username: "readonly_user"
password: "readonly_password"

# Safety
readonly: true
timeout: 30

📌 Notes:

Always use a read-only user for safety.

timeout prevents queries from running forever.

Future: we can enforce row-level or column-level security here.



---

🔹 llm_config.yaml

# LLM Configuration
provider: "weaviate"   # options: chroma, weaviate, graph

# In-house LLM API (via Weaviate integration)
weaviate:
  host: "http://weaviate.company.com"
  api_key: "YOUR_API_KEY"
  class_name: "OTCKnowledge"
  top_k: 5

# Local ChromaDB fallback
chroma:
  persist_directory: "./chroma_store"
  collection_name: "otc_copilot"
  embedding_model: "./models/all-MiniLM-L6-v2"
  top_k: 5

# GraphDB (Neo4j) for schema reasoning
graph:
  uri: "bolt://localhost:7687"
  user: "neo4j"
  password: "password"
  database: "neo4j"

📌 Notes:

provider determines which retriever backend is used.

Switching from chroma → weaviate → graph requires no code changes, only config change.



---

✅ Benefits of Central Config

✔ Separation of concerns → devs don’t hardcode DB/LLM settings.
✔ Flexibility → switch between ChromaDB, Weaviate, GraphDB.
✔ Security → read-only DB creds, API keys stored outside code.
✔ Scalability → ops teams can tune retrieval (e.g., top_k) easily.


---

👉 Do you want me to also prepare a README.md for config/ that explains each YAML file in plain English for your ops colleagues (non-technical users), so they know what they can/cannot safely change?

---
Perfect 👍 here’s the config/README.md that explains everything in the config/ folder in plain English so even non-technical ops colleagues can maintain it safely.


---

📂 config/ – Configuration Guide for OTC Ops Copilot

The config/ folder contains all the settings for how OTC Ops Copilot connects to the database, LLM (AI model), and retrievers.
These files are written in YAML format – easy to read and edit with a text editor.


---

📌 Files in this folder

🔹 chromadb_config.yaml

Controls how ChromaDB (local vector store) works.

Key fields:

persist_directory → where embeddings are stored on disk.

collection_name → the collection name (keep it otc_copilot).

embedding_model → path to the embedding model (e.g., ./models/all-MiniLM-L6-v2).

top_k → how many documents to fetch per query.



📖 When to edit:

Change persist_directory if moving ChromaDB files.

Change top_k if you want more or fewer matches per question.



---

🔹 db_config.yaml

Defines how OTC Copilot connects to the MS SQL database.

Key fields:

server → your database server address.

database → the database name (e.g., OTC_Trade_Confirmation).

username, password → must be read-only credentials.

readonly → keep this true (safety rule).

timeout → stops long-running queries.



📖 When to edit:

Only if DB server/credentials change.

⚠️ Always use readonly_user → never give write access.



---

🔹 llm_config.yaml

Chooses which backend retriever OTC Copilot uses:

chroma → lightweight, local testing.

weaviate → enterprise vector DB (integrates with in-house LLM).

graph → Neo4j GraphDB (for schema reasoning).


Key fields under each provider:

weaviate.host, weaviate.api_key → connection to Weaviate.

chroma.persist_directory, embedding_model → local Chroma setup.

graph.uri, graph.user, graph.password → Neo4j credentials.



📖 When to edit:

Switch provider to chroma, weaviate, or graph.

Update connection details when infra changes.



---

📌 Best Practices

✅ Keep readonly credentials for DB.

✅ Store API keys in a secure vault if possible.

✅ Version control YAMLs, but don’t commit real passwords → use placeholders.

✅ Document changes (who changed configs & why).



---

📌 Example: Switching Backends

If today you’re using ChromaDB, but want to try Weaviate, just edit:

# llm_config.yaml
provider: "weaviate"

No code changes needed 🚀.


---

✅ In short:
The config/ folder makes OTC Ops Copilot flexible and safe — DB admins and ops teams can manage connections without touching the Python code.
---
