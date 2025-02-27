"""Test configuration and fixtures."""
import os
from datetime import datetime

import pytest
from airflow.models import DagBag
from pymongo import MongoClient


@pytest.fixture(scope="session")
def test_dag():
    """Fixture for test DAG."""
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    return dagbag.get_dag(dag_id="sql_scheduler_dag")


@pytest.fixture(scope="session")
def mock_mongodb():
    """Fixture for mock MongoDB connection."""
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGODB_DATABASE") + "_test"]
    yield db
    client.drop_database(db.name)
    client.close()


@pytest.fixture
def sample_sql_query():
    """Fixture for sample SQL query."""
    return "SELECT * FROM test_table LIMIT 10"


@pytest.fixture
def execution_date():
    """Fixture for execution date."""
    return datetime(2025, 2, 27)


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ.update({
        "MONGODB_URI": "mongodb://localhost:27017/",
        "MONGODB_DATABASE": "test_db",
        "REQUEST_TIMEOUT": "30",
        "MAX_RETRIES": "3",
        "RETRY_DELAY": "5",
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "test.log",
        "CACHE_ENABLED": "true",
        "CACHE_TTL": "3600"
    })
    yield
    # Clean up is handled by pytest
