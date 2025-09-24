import pytest
from core.engine import Engine

def test_trade_summary():
    engine = Engine(backend="chroma")
    result = engine.ask("Show number of confirmed trades today")
    assert "sql" in result
    assert "result" in result
    assert isinstance(result["result"], list)
