"""Tests for SQL Scheduler DAG."""
import os
from datetime import datetime
from unittest import TestCase, mock

import pytest
from airflow.models import DagBag, TaskInstance
from airflow.utils.session import create_session
from airflow.utils.state import State

# Import the DAG from your project
from dags.sql_scheduler_dag import default_args


class TestSQLSchedulerDAG(TestCase):
    """Test cases for SQL Scheduler DAG."""

    def setUp(self):
        """Set up test environment."""
        self.dagbag = DagBag(dag_folder="dags/", include_examples=False)
        self.dag = self.dagbag.get_dag(dag_id="sql_scheduler_dag")
        self.test_date = datetime(2025, 2, 27)

    def test_dag_loaded(self):
        """Test that the DAG is loaded correctly."""
        assert self.dagbag.import_errors == {}
        assert self.dag is not None
        assert len(self.dag.tasks) > 0

    def test_dag_structure(self):
        """Test the structure of the DAG."""
        task_ids = [task.task_id for task in self.dag.tasks]
        expected_tasks = ["validate_sql", "execute_sql", "process_results"]
        for task in expected_tasks:
            assert task in task_ids

    def test_dependencies(self):
        """Test task dependencies are set correctly."""
        tasks = {task.task_id: task for task in self.dag.tasks}
        assert tasks["execute_sql"].upstream_task_ids == {"validate_sql"}
        assert tasks["process_results"].upstream_task_ids == {"execute_sql"}

    @mock.patch("dags.sql_scheduler_dag.validate_sql_query")
    def test_validate_sql_task(self, mock_validate):
        """Test SQL validation task."""
        mock_validate.return_value = True
        task = self.dag.get_task("validate_sql")
        ti = TaskInstance(task=task, execution_date=self.test_date)
        with create_session() as session:
            ti.run(session=session)
            assert ti.state == State.SUCCESS

    @mock.patch("dags.sql_scheduler_dag.execute_sql_query")
    def test_execute_sql_task(self, mock_execute):
        """Test SQL execution task."""
        mock_execute.return_value = {"status": "success", "rows_affected": 10}
        task = self.dag.get_task("execute_sql")
        ti = TaskInstance(task=task, execution_date=self.test_date)
        with create_session() as session:
            ti.run(session=session)
            assert ti.state == State.SUCCESS

    def test_env_variables(self):
        """Test environment variables are set correctly."""
        required_env_vars = [
            "MONGODB_URI",
            "MONGODB_DATABASE",
            "REQUEST_TIMEOUT",
            "MAX_RETRIES"
        ]
        for var in required_env_vars:
            assert var in os.environ, f"Missing environment variable: {var}"

    def test_retry_config(self):
        """Test retry configuration."""
        assert default_args['retries'] == int(os.getenv("MAX_RETRIES", 3))
        retry_seconds = default_args['retry_delay'].total_seconds()
        assert retry_seconds == int(os.getenv("RETRY_DELAY", 5)) * 60

    @pytest.mark.security
    def test_security_config(self):
        """Test security configurations."""
        # Test database URI encryption
        db_uri = os.getenv("MONGODB_URI")
        assert db_uri is not None
        assert not db_uri.startswith("mongodb://localhost")

        # Test request timeout
        timeout = int(os.getenv("REQUEST_TIMEOUT", 30))
        assert timeout > 0
        assert timeout <= 60  # Maximum allowed timeout

    @pytest.mark.integration
    def test_end_to_end_flow(self):
        """Test the entire DAG flow."""
        dag_run = self.dag.create_dagrun(
            state=State.RUNNING,
            execution_date=self.test_date,
            run_type="manual"
        )
        dag_run.run()
        assert dag_run.state == State.SUCCESS
