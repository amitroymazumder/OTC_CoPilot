import streamlit as st
from core.engine import Engine
from core.visualizer import plot_table, plot_chart

st.title("OTC Ops Copilot")

backend = st.sidebar.selectbox("Retriever Backend", ["chroma", "weaviate", "graph"])
engine = Engine(backend=backend)

query = st.text_area("Enter your question (NL):")
if st.button("Run"):
    output = engine.ask(query)
    if "error" in output:
        st.error(output["error"])
    else:
        st.code(output["sql"], language="sql")
        st.dataframe(output["result"])
        st.plotly_chart(plot_chart(output["result"]))
