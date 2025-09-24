import yaml
import requests

def generate_sql(question: str, context: list) -> str:
    """
    Generates SQL using LLM + retrieved context.

    - For in-house LLM, call internal API.
    - For external (POC), could call Gemini/OpenAI.

    context: list of schema/rules/master data strings.
    """
    prompt = f"""
    You are a SQL generation assistant.
    Question: {question}
    Use the following database context:
    {context}

    Generate a safe SQL SELECT query (no INSERT/DELETE/UPDATE).
    """

    # Example: Call in-house LLM API (replace with real endpoint)
    try:
        response = requests.post(
            "http://inhouse-llm.local/api/v1/generate",
            json={"prompt": prompt, "max_tokens": 512}
        )
        sql = response.json().get("text", "").strip()
    except Exception:
        # Fallback for POC
        sql = "SELECT TOP 10 * FROM Trades"

    return sql
