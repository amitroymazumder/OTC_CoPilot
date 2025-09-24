import pytest
from core.sql_validator import validate_sql

def test_valid_select():
    sql = "SELECT * FROM Trades WHERE status = 'Confirmed'"
    result = validate_sql(sql)
    assert result["valid"] is True

def test_invalid_insert():
    sql = "INSERT INTO Trades VALUES (1, 'test')"
    result = validate_sql(sql)
    assert result["valid"] is False

def test_block_dangerous():
    sql = "DROP TABLE Trades"
    result = validate_sql(sql)
    assert result["valid"] is False
