"""Tests for SQL validation utilities."""
import pytest

from utils.sql_validator import (
    validate_sql_query,
    check_sql_injection,
    validate_query_timeout
)


def test_valid_select_query():
    """Test validation of a valid SELECT query."""
    query = "SELECT * FROM users WHERE age > 18"
    assert validate_sql_query(query) is True


def test_invalid_syntax():
    """Test validation of query with invalid syntax."""
    query = "SELEC * FORM users"  # Intentional typos
    with pytest.raises(ValueError) as exc:
        validate_sql_query(query)
    assert "Invalid SQL syntax" in str(exc.value)


def test_forbidden_operations():
    """Test validation against forbidden operations."""
    forbidden_queries = [
        "DROP TABLE users",
        "TRUNCATE TABLE logs",
        "DELETE FROM users",
        "UPDATE users SET status='inactive'",
    ]
    for query in forbidden_queries:
        with pytest.raises(ValueError) as exc:
            validate_sql_query(query)
        assert "Operation not allowed" in str(exc.value)


def test_sql_injection_prevention():
    """Test SQL injection detection."""
    malicious_queries = [
        "SELECT * FROM users WHERE id = 1; DROP TABLE users;",
        "SELECT * FROM users WHERE username = 'admin' OR '1'='1'",
        "SELECT * FROM users; DELETE FROM audit_log;--",
    ]
    for query in malicious_queries:
        assert check_sql_injection(query) is False


def test_query_timeout_validation():
    """Test query timeout validation."""
    # Test valid queries
    valid_queries = [
        "SELECT * FROM users LIMIT 100",
        "SELECT COUNT(*) FROM events",
    ]
    for query in valid_queries:
        assert validate_query_timeout(query) is True

    # Test potentially slow queries
    slow_queries = [
        "SELECT * FROM large_table",  # Missing LIMIT
        "SELECT * FROM table1 JOIN table2 JOIN table3",  # Multiple joins
        "SELECT * FROM events WHERE timestamp >= NOW() - INTERVAL '1 year'"
    ]
    for query in slow_queries:
        with pytest.raises(ValueError) as exc:
            validate_query_timeout(query)
        assert "Query may timeout" in str(exc.value)


@pytest.mark.parametrize("query,expected", [
    ("SELECT * FROM users LIMIT 10", True),
    ("SELECT * FROM users; DELETE FROM users;", False),
    ("DROP DATABASE production;", False),
    ("SELECT * FROM users WHERE id = '1' OR '1'='1'", False),
])
def test_query_validation_cases(query, expected):
    """Test various query validation cases."""
    if expected:
        assert validate_sql_query(query) is True
    else:
        with pytest.raises(ValueError):
            validate_sql_query(query)


def test_query_complexity():
    """Test query complexity validation."""
    complex_query = """
    WITH RECURSIVE cte AS (
        SELECT id, parent_id, name, 1 as level
        FROM categories
        WHERE parent_id IS NULL
        UNION ALL
        SELECT c.id, c.parent_id, c.name, cte.level + 1
        FROM categories c
        JOIN cte ON c.parent_id = cte.id
    )
    SELECT * FROM cte;
    """
    with pytest.raises(ValueError) as exc:
        validate_sql_query(complex_query)
    assert "Query too complex" in str(exc.value)
