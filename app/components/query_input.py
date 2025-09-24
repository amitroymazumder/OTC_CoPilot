import streamlit as st

def query_box():
    """
    Renders a text area for the user to input a natural language question.
    """
    return st.text_area(
        "Enter your question in Natural Language:",
        placeholder="e.g., Show me all trades confirmed today grouped by counterparty"
    )
