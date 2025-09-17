# README for olivium-dev/badge-service

# Badge Microservice

A RESTful microservice for managing user badges and achievements built with FastAPI and PostgreSQL.

## Overview

The Badge Microservice provides a robust API for managing user badges in a microservices architecture. It allows for badge assignment, retrieval, and management with full CRUD operations.

## Features

- 🏆 Badge Management (Create, Read, Update, Delete)
- 👤 User-specific badge assignments
- 📝 Configurable badge definitions
- 🔒 Secure database operations
- 📚 Swagger/OpenAPI documentation
- 🚀 Simple and lightweight implementation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Documentation**: Swagger/OpenAPI

## Prerequisites

- Python 3.9+
- PostgreSQL
- Git

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd Badge_Microservice
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with the following variables
DATABASE_URL="postgresql://postgres:your_password@localhost:5432/badge"
CONFIGURATION='[{"badgeId":"1","badgeName":"Verified","badgeDescription":"The Verified badge is awarded to users or accounts that have been authenticated to confirm their identity"},{"badgeId":"2","badgeName":"Extra verified","badgeDescription":"The Extra Verified badge is awarded to users who have completed additional verification steps"}]'
```

## Running the Application

### Local Development
```bash
python Main.py
```
The server will start at `http://localhost:5004`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user-badge` | Create a new badge assignment |
| GET | `/user-badge/{user_id}` | Get user's badges |
| DELETE | `/user-badge/{user_id}` | Delete user's badge |
| GET | `/badges-list` | Get all available badges |
| GET | `/health` | Health check endpoint |

### Example Requests

#### Create Badge Assignment
```bash
curl -X POST "http://localhost:5004/user-badge" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "badge_id": "1"}'
```

#### Get User's Badges
```bash
curl -X GET "http://localhost:5004/user-badge/user123"
```

#### Get All Available Badges
```bash
curl -X GET "http://localhost:5004/badges-list"
```

## Documentation

API documentation is available via Swagger UI at `http://localhost:5004/docs`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection URL | Yes |
| CONFIGURATION | JSON string of badge definitions | Yes |

## Badge Configuration

The CONFIGURATION environment variable defines all available badges in the system. Each badge has:

- `badgeId`: Unique identifier for the badge
- `badgeName`: Display name of the badge
- `badgeDescription`: Detailed description of what the badge represents

When assigning badges to users, the system validates that the badge ID exists in this configuration.

## Error Handling

The API includes proper error handling for:
- Invalid badge IDs
- Missing required parameters
- Database connection issues
- Duplicate badge assignments

## Support

For support, please open an issue in the repository or contact the development team. 