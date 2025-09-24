create a **`loaders/README.md`** that explains everything about the loaders and the unified training script.
This will serve as documentation for your team so they know exactly how to use and extend these files.

---

# 📂 `loaders/` – Knowledge Loaders for OTC Ops Copilot

The `loaders/` folder contains the **adapters** that load OTC Copilot knowledge (schema, relationships, master data, rules) into different backends:

* **ChromaDB** → lightweight local vector store.
* **Weaviate** → enterprise-grade vector DB (connects with in-house LLM).
* **GraphDB (Neo4j)** → schema-aware reasoning, perfect for complex joins.

Each loader exposes a **unified retriever interface**:

```python
retriever = init()
context = retriever.query("Show me all confirmed trades today", top_k=5)
```

---

## 📌 Files & Responsibilities

### 🔹 `loader_chromadb.py`

* Loads YAML knowledge into **ChromaDB**.
* Uses **SentenceTransformer embeddings** (`all-MiniLM-L6-v2`) from a **local model folder** (`./models/all-MiniLM-L6-v2`).
* Workflow:

  1. Load YAMLs → flatten into text documents.
  2. Insert into Chroma collection `otc_copilot`.
  3. Expose `query(question, top_k)` which runs semantic search.
* Best for:

  * Local development / POCs.
  * When Hugging Face downloads are blocked (model hosted locally).

---

### 🔹 `loader_weaviate.py`

* Loads YAML knowledge into **Weaviate**.
* Creates a class called `OTCKnowledge` (if not already present).
* Inserts knowledge as text objects with `content` property.
* Exposes `query(question, top_k)` which uses Weaviate’s **nearText search**.
* Best for:

  * Enterprise deployments.
  * Seamless integration with in-house LLM RAG pipelines.

---

### 🔹 `loader_graphdb.py`

* Loads YAML knowledge into **Neo4j GraphDB**.
* Creates:

  * `(:Table)` nodes for each table.
  * `(:Column)` nodes linked with `[:HAS_COLUMN]`.
  * `(:PrimaryKey)` nodes linked with `[:HAS_PK]`.
  * `[:FK]` relationships between tables.
  * `(:MasterData)` nodes for statuses, event types, etc.
  * `(:Rule)` nodes for business rules.
* Exposes `query(question, top_k)` → currently returns schema samples (extendable to full **Graph RAG** with Cypher query reasoning).
* Best for:

  * Complex schemas with 100s of tables.
  * Cases where LLM needs **explicit schema relationships**.

---

### 🔹 `train_loader.py`

* **One script to load knowledge into all 3 backends.**
* Reads YAMLs from `./knowledge/`.
* Supports CLI options:

  ```bash
  python train_loader.py --only chroma     # train only Chroma
  python train_loader.py --only weaviate   # train only Weaviate
  python train_loader.py --only graph      # train only GraphDB
  python train_loader.py --only all        # train all (default)
  ```
* Optional: can be extended with `--data <path>` to train from a different YAML folder.

---

## 📌 Flow of Control

1. **YAML Knowledge Base** (`knowledge/*.yaml`)

   * Schema (tables + columns)
   * Relationships (FKs)
   * Primary keys
   * Master data (statuses, event types, product types)
   * Rules

2. **`train_loader.py`**

   * Flattens YAMLs into documents.
   * Pushes documents into **ChromaDB**, **Weaviate**, and **Neo4j**.

3. **Retriever**

   * `retriever.query("Show trades confirmed today")` → returns context.

4. **Engine** (`core/engine.py`)

   * Passes question + context → LLM → SQL → executes in MS SQL.

---

## 📌 When to Use Which Backend?

* **ChromaDB**
  ✅ Best for local testing, small deployments.
  ❌ Limited scaling for very large datasets.

* **Weaviate**
  ✅ Production-ready, scalable.
  ✅ Integrates with in-house LLM pipelines.
  ❌ Requires infra setup.

* **GraphDB (Neo4j)**
  ✅ Best for **complex schemas** with 100s of tables.
  ✅ Explicit schema-awareness → helps avoid bad joins.
  ❌ More complex to maintain.

---

## 📌 Example Usage

```python
from loaders import loader_chromadb, loader_weaviate, loader_graphdb

# Chroma
chroma_retriever = loader_chromadb.init()
print(chroma_retriever.query("List confirmed trades", top_k=3))

# Weaviate
weaviate_retriever = loader_weaviate.init()
print(weaviate_retriever.query("Show settlement events", top_k=3))

# Graph
graph_retriever = loader_graphdb.init()
print(graph_retriever.query("Which tables relate trades and counterparties?", top_k=5))
```

---

✅ In short:

* **`loader_chromadb.py`** → local vector store.
* **`loader_weaviate.py`** → enterprise RAG pipeline.
* **`loader_graphdb.py`** → schema-aware reasoning.
* **`train_loader.py`** → one script to sync all 3 backends.

---


