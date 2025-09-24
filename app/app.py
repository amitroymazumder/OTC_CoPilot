import streamlit as st
from core.engine import Engine
from core.visualizer import plot_table, plot_chart

# App Title
st.set_page_config(page_title="OTC Ops Copilot", layout="wide")
st.title("📊 OTC Ops Copilot")

# Sidebar Options
backend = st.sidebar.selectbox(
    "Retriever Backend",
    ["chroma", "weaviate", "graph"],
    help="Choose how knowledge is retrieved: ChromaDB (local), Weaviate (enterprise), or Graph (Neo4j schema reasoning)"
)

engine = Engine(backend=backend)

# Query Input
from app.components.query_input import query_box
question = query_box()

if st.button("Run Query"):
    output = engine.ask(question)

    if "error" in output:
        st.error(output["error"])
    else:
        st.subheader("🔹 Generated SQL")
        st.code(output["sql"], language="sql")

        st.subheader("📋 Results")
        from app.components.results_table import show_table
        show_table(output["result"])

        st.subheader("📈 Visualization")
        from app.components.charts import show_charts
        show_charts(output["result"])
