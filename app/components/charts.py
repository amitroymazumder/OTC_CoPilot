import streamlit as st
import pandas as pd
import plotly.express as px

def show_charts(result):
    """
    Creates a simple chart from SQL result if it has numeric columns.
    """
    if not isinstance(result, pd.DataFrame):
        df = pd.DataFrame(result)
    else:
        df = result

    if df.empty:
        st.warning("No data available to plot")
        return

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) >= 1:
        col1 = numeric_cols[0]
        chart = px.histogram(df, x=col1)
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No numeric columns to visualize")
