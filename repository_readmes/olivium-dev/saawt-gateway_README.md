# README for olivium-dev/saawt-gateway

﻿# SAAWT Gateway

API Gateway service for the SAAWT platform.

## SQLite Logging System

The gateway uses SQLite for logging API requests and application events. The following components are involved:

- **NLog Configuration**: Uses NLog.Database to write logs to SQLite database tables
- **Database Path**: Set via the `SQLiteDbPath` environment variable (default: `log.db`)
- **Log Tables**:
  - `ApiLogs`: Captures API request/response details with correlation IDs
  - `InnerLogs`: Captures application internal logs
  - `SimpleLog`: Simplified log format for testing/debugging

## Test Scripts

Several scripts are available to test and debug the logging system:

### 1. Basic Logging Test
```bash
./test_logging.sh [API_URL=http://localhost:8080]
```
Tests the logging pipeline by making API calls with a unique correlation ID and verifying logs are written.

### 2. Docker Local Test
```bash
./run_local_test.sh
```
Builds and runs the application in a Docker container with proper volume mapping to ensure logs are accessible from the host.

### 3. Direct SQLite Test
```bash
./test_local_db.sh
```
Tests direct SQLite database writing to verify database access permissions and structure.

### 4. Container SQLite Fix
```bash
./fix_container_sqlite.sh
```
Installs SQLite tools in a running container, checks the database setup, and inserts test records directly.

### 5. Full Diagnostic Test
```bash
./final_fix.sh
```
Complete diagnostic tool that builds a special Docker image with enhanced logging and SQLite tools to troubleshoot logging issues.

## Common Issues

- **Missing Log Entries**: Ensure NLog targets are configured with the correct connection string and path
- **Permission Issues**: SQLite database directory must be writable by the application
- **Container Volume Mapping**: When running in Docker, ensure the database directory is properly volume-mapped for persistence
- **NLog Configuration**: Set `internalLogLevel="Debug"` and `internalLogFile="path"` to diagnose NLog issues

## Development

To start the service locally:

```bash
dotnet run
```

To build and run in Docker:

```bash
docker build -t saawt-gateway .
docker run -p 8080:80 -v "$(pwd)/data:/app/data" -e SQLiteDbPath=/app/data/log.db saawt-gateway
```

# SAAWT Gateway API Test Script

This project contains scripts to test the SAAWT Gateway API by creating test users, managing wallets, and purchasing credits.

## Prerequisites

- Python 3.6 or higher
- SAAWT Gateway API running (default: http://localhost:5000)

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Test Script

To run the main test script that performs all API operations:

```
python setup_test_users.py
```

This script performs the following operations:
1. Creates TestUser1 and TestUser2 (signup)
2. Gets TestUser1 wallets
3. Gets TestUser2 wallets
4. Adds 1000 USD to TestUser1 wallet
5. Adds 1000 USD to TestUser2 wallet
6. Makes TestUser1 buy 100 credits

### Validating the Test Script

To run the validation environment that tests the script and verifies results:

```
python validate_setup.py
```

The validation script will:
1. Check Python version and dependencies
2. Verify API availability
3. Run the main test script
4. Validate user creation and login
5. Validate wallet retrieval and balances

## Configuration

Edit the `BASE_URL` variable in `setup_test_users.py` if your API is running at a different location:

```python
# Base URL for the API
BASE_URL = "http://localhost:5000"  # Change to your API's base URL
```

## SQLite Database Persistence

The application uses SQLite for logging API requests and responses. To ensure data persistence:

### Local Development
- The database file is stored as `log.db` in the application root by default
- You can back up this file manually when needed: `cp log.db log.db.bak`

### Docker Deployment
- The database is stored in a persistent volume at `/app/data/log.db` inside the container
- The volume is mounted from the host system to preserve data between deployments
- The path is configurable via the `SQLiteDbPath` environment variable

### GitHub Workflow Deployment
When deploying using the GitHub workflow:
1. A host directory is created for database persistence (default: `/data/saawt-gateway/db`)
2. This directory is mounted to the Docker container's `/app/data` directory
3. The SQLite database is stored in this persistent location
4. New deployments will use the existing database if one exists

To modify the database location when deploying, change the `db_volume_path` parameter in the GitHub workflow.