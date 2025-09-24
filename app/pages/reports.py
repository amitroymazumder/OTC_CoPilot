import streamlit as st
from core.engine import Engine
from services.scheduler import schedule_report

st.set_page_config(page_title="OTC Reports", layout="wide")
st.title("📝 Scheduled Reports")

backend = st.sidebar.selectbox("Retriever Backend", ["chroma", "weaviate", "graph"])
engine = Engine(backend=backend)

st.subheader("Schedule a Report")
report_name = st.text_input("Report Name")
question = st.text_area("Enter your report query in Natural Language")
schedule_time = st.time_input("Select time of day")

if st.button("Schedule Report"):
    schedule_report(report_name, question, schedule_time)
    st.success(f"Report '{report_name}' scheduled at {schedule_time}")
