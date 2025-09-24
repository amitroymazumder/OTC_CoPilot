from weasyprint import HTML
import pandas as pd
from io import BytesIO
import os

OUTPUT_DIR = "./reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pdf(report_name, sql, df: pd.DataFrame):
    """
    Generates a PDF report with:
    - Report name
    - Generated SQL
    - Data table
    """
    html_content = f"""
    <html>
    <head><style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ color: #003366; }}
        table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 4px; }}
    </style></head>
    <body>
        <h1>OTC Report: {report_name}</h1>
        <p><b>Generated SQL:</b><br><code>{sql}</code></p>
        <h2>Data</h2>
        {df.to_html(index=False)}
    </body>
    </html>
    """

    filepath = os.path.join(OUTPUT_DIR, f"{report_name}.pdf")
    HTML(string=html_content).write_pdf(filepath)
    return filepath

def generate_excel(report_name, df: pd.DataFrame):
    """
    Generates an Excel report.
    """
    filepath = os.path.join(OUTPUT_DIR, f"{report_name}.xlsx")
    df.to_excel(filepath, index=False)
    return filepath
