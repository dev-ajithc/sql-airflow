"""
DAG to schedule and execute SQL scripts with email notifications.
"""
from datetime import timedelta
import os
from pathlib import Path

from airflow import DAG
from airflow.utils.dates import days_ago
from dotenv import load_dotenv

from operators.sql_email_operator import SQLEmailOperator

# Load environment variables
load_dotenv()

# Security: Read sensitive data from environment variables
PG_CONN_ID = "postgres_default"
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')

# Define default arguments with proper retry settings
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': int(os.getenv('MAX_RETRIES', 3)),
    'retry_delay': timedelta(minutes=int(os.getenv('RETRY_DELAY', 5))),
    'execution_timeout': timedelta(
        seconds=int(os.getenv('REQUEST_TIMEOUT', 30))
    ),
}

# Read SQL query from file
sql_file_path = Path(__file__).parents[1] / 'sql' / 'example_query.sql'
with open(sql_file_path, 'r') as f:
    sql_query = f.read()

# Create DAG
with DAG(
    'sql_scheduler',
    default_args=default_args,
    description='Schedule and execute SQL scripts with email notifications',
    schedule_interval='0 0 * * *',  # Run daily at midnight
    start_date=days_ago(1),
    catchup=False,
    tags=['sql', 'scheduled', 'email'],
) as dag:

    # Task to execute SQL query and send email
    execute_sql = SQLEmailOperator(
        task_id='execute_sql_query',
        postgres_conn_id=PG_CONN_ID,
        sql=sql_query,
        email_to=EMAIL_RECIPIENTS,
        email_subject='Daily SQL Query Results',
        # Implement proper error handling
        on_failure_callback=lambda context: print(
            f"Task failed: {context.get('exception')}"
        ),
        # Add task documentation
        doc_md="""
        # SQL Query Execution Task with Email Notifications
        This task executes a scheduled SQL query and sends results via email.

        ## Error Handling
        - Retries: {retries}
        - Retry Delay: {retry_delay} min

        ## Email Configuration
        - Recipients: Configured via EMAIL_RECIPIENTS env var
        - Subject: Daily SQL Query Results
        """.format(
            retries=default_args['retries'],
            retry_delay=default_args['retry_delay'].seconds // 60,
        )
    )
