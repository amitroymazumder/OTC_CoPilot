import streamlit as st
from core.engine import Engine
from core.visualizer import plot_chart

st.set_page_config(page_title="OTC Dashboards", layout="wide")
st.title("📊 Prebuilt Dashboards")

backend = st.sidebar.selectbox("Retriever Backend", ["chroma", "weaviate", "graph"])
engine = Engine(backend=backend)

# Example prebuilt dashboard: Daily confirmed trades
st.subheader("Trades Confirmed per Day")
output = engine.ask("Show me number of confirmed trades per day in the last week")
if "error" not in output:
    st.code(output["sql"], language="sql")
    st.dataframe(output["result"])
    st.plotly_chart(plot_chart(output["result"]))
