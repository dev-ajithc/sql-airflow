# SQL Airflow Scheduler

A secure and efficient solution for scheduling SQL queries using Apache Airflow. This project provides automated execution of SQL scripts with proper security measures, error handling, and monitoring capabilities.

## Features

- Automated SQL query scheduling and execution
- Secure database connection handling
- Comprehensive error handling and logging
- Rate limiting and retry mechanisms
- Input validation and sanitization
- Configurable execution parameters
- Monitoring and alerting capabilities

## Prerequisites

- Python 3.8 or higher
- Apache Airflow
- MongoDB
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sql-airflow.git
cd sql-airflow
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables

The following environment variables need to be configured in your `.env` file:

- `MONGODB_URI`: MongoDB connection string
- `MONGODB_DATABASE`: Target database name
- `REQUEST_TIMEOUT`: Timeout for database requests
- `MAX_RETRIES`: Maximum retry attempts
- `RETRY_DELAY`: Delay between retries
- `LOG_LEVEL`: Logging level (INFO/DEBUG/ERROR)
- `LOG_FILE`: Log file location
- `CACHE_ENABLED`: Enable/disable caching
- `CACHE_TTL`: Cache time-to-live

## Project Structure

```
sql-airflow/
├── dags/
│   └── sql_scheduler_dag.py    # Airflow DAG definition
├── sql/
│   └── example_query.sql       # SQL query templates
├── tests/
│   ├── __init__.py            # Test package marker
│   ├── conftest.py            # Test configuration and fixtures
│   ├── test_sql_scheduler_dag.py  # DAG tests
│   └── test_sql_validator.py   # SQL validation tests
├── .env.example                # Environment variables template
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Usage

1. Place your SQL queries in the `sql/` directory
2. Configure the DAG parameters in `dags/sql_scheduler_dag.py`
3. Start the Airflow scheduler:
```bash
airflow scheduler
```

4. Access the Airflow web interface to monitor your DAGs:
```bash
airflow webserver
```

## Testing

The project includes a comprehensive test suite covering various aspects of the application.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test categories
pytest -v -m security        # Security tests
pytest -v -m integration    # Integration tests

# Run tests with detailed output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Test Categories

1. **DAG Tests** (`test_sql_scheduler_dag.py`):
   - DAG structure validation
   - Task dependencies
   - Execution flow
   - Retry configurations
   - Environment setup

2. **SQL Validation Tests** (`test_sql_validator.py`):
   - Query syntax validation
   - SQL injection prevention
   - Query timeout checks
   - Forbidden operations
   - Query complexity analysis

3. **Security Tests**:
   - Database connection security
   - Environment variable validation
   - Access control checks
   - Rate limiting verification

4. **Integration Tests**:
   - End-to-end workflow
   - Database interactions
   - External service connections

### Test Configuration

- Test environment variables are managed in `conftest.py`
- Mock database connections for testing
- Automatic test database cleanup
- Configurable test timeouts
- Comprehensive test fixtures

## Security Measures

- Secure hash functions (SHA-256) for data integrity
- Input validation and sanitization
- Rate limiting for database requests
- Environment variables for sensitive data
- Comprehensive logging and monitoring
- Latest security package versions
- Access control implementation
- Regular security updates

## Development

### Code Quality Tools

The project uses the following code quality tools:

- flake8: Code style and quality checker
- isort: Import statement organizer
- mypy: Static type checker
- pytest: Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines

1. Write tests for new features
2. Maintain test coverage above 80%
3. Follow PEP 8 style guide
4. Document all functions and classes
5. Add security tests for sensitive operations

## License

[Your License Here]

## Support

For support, please open an issue in the GitHub repository.
