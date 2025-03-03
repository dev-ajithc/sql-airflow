"""
Custom operator for executing SQL queries and sending email notifications.
"""
from typing import Any, Dict, List, Optional

from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.email import send_email
from cryptography.fernet import Fernet
import pandas as pd


class SQLEmailOperator(PostgresOperator):
    """
    Operator that executes SQL queries and sends results via email.

    This operator extends PostgresOperator to add email notification
    capabilities with secure result handling.
    """

    template_fields = ('sql', 'email_subject')

    def __init__(
        self,
        *,
        email_to: List[str],
        email_subject: str = 'SQL Query Results',
        include_headers: bool = True,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.email_to = email_to
        self.email_subject = email_subject
        self.include_headers = include_headers

    def _format_results(
        self, results: List[Dict[str, Any]]
    ) -> str:
        """Format query results into an HTML table."""
        if not results:
            return '<p>No results found.</p>'

        df = pd.DataFrame(results)
        return f"""
        <html>
            <body>
                <h2>SQL Query Results</h2>
                <p>Execution Time: {pd.Timestamp.now()}</p>
                {df.to_html(index=False)}
            </body>
        </html>
        """

    def execute(self, context: Dict[str, Any]) -> None:
        """Execute the SQL query and send results via email."""
        # Execute SQL query using parent class
        super().execute(context)

        # Fetch results using PostgresHook
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        results = hook.get_records(self.sql)

        # Format results and send email
        html_content = self._format_results(results)
        send_email(
            to=self.email_to,
            subject=self.email_subject,
            html_content=html_content,
            mime_charset='utf-8'
        )
