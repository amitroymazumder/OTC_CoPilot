import re

def validate_sql(sql: str) -> bool:
    """
    Ensures that generated SQL is safe:
    - Only SELECT queries
    - No DML/DDL statements
    - Basic syntax check
    """
    sql_clean = sql.strip().lower()

    # Disallow dangerous keywords
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in sql_clean for word in forbidden):
        return False

    # Must start with SELECT
    if not sql_clean.startswith("select"):
        return False

    # Simple regex to ensure valid FROM clause
    if not re.search(r"from\s+\w+", sql_clean):
        return False

    return True
