import pyodbc
import pandas as pd
import yaml

def get_connection():
    """
    Establish a read-only connection to MS SQL Server.
    db_config.yaml must have:
    DRIVER, SERVER, DATABASE, USERNAME, PASSWORD
    """
    with open("config/db_config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    conn = pyodbc.connect(
        f"DRIVER={cfg['DRIVER']};"
        f"SERVER={cfg['SERVER']};"
        f"DATABASE={cfg['DATABASE']};"
        f"UID={cfg['USERNAME']};"
        f"PWD={cfg['PASSWORD']};"
    )
    return conn

def run_query(sql: str):
    """
    Executes a validated SELECT query against MS SQL.
    Returns a Pandas DataFrame.
    """
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df
