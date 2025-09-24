import streamlit as st
import pandas as pd

def show_table(result):
    """
    Renders SQL result as a Streamlit dataframe.
    `result` should be a list of dicts or pandas DataFrame.
    """
    if isinstance(result, pd.DataFrame):
        st.dataframe(result, use_container_width=True)
    else:
        st.dataframe(pd.DataFrame(result), use_container_width=True)
