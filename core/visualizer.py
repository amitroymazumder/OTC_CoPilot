import plotly.express as px
import pandas as pd

def plot_table(df: pd.DataFrame):
    """
    Returns a simple DataFrame for Streamlit to render.
    """
    return df

def plot_chart(df: pd.DataFrame):
    """
    Creates a chart if data is numeric.
    - If multiple numeric cols → bar chart
    - If 1 numeric col → histogram
    """
    if df.empty:
        return None

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) == 0:
        return None

    if len(numeric_cols) >= 2:
        return px.bar(df, x=numeric_cols[0], y=numeric_cols[1])
    else:
        return px.histogram(df, x=numeric_cols[0])
