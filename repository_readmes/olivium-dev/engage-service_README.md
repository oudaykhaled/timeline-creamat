# README for olivium-dev/engage-service

# Engage Service

A high-performance microservice for managing user interactions and engagements.

## Features

- Dynamic configuration of interaction types (boolean or enum)
- Automatic database table creation and migration
- RESTful API for managing interactions
- Production-ready with proper error handling and logging
- Supports millions of interactions efficiently

## Configuration

The service is configured through environment variables:

### Required Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg2://postgres:newpassword@localhost:5432/engage

# Server Configuration
PORT=8080
GIN_MODE=release

# Interaction Configuration (JSON array of interaction types)
INTERACTION_CONFIG=[{"name":"favorite","type":"boolean"},{"name":"like","type":"boolean"},{"name":"pass","type":"boolean"},{"name":"visit","type":"boolean"} ,{"name":"block","type":"boolean"}]
```

### Optional Database Configuration (used if DATABASE_URL is not set)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=newpassword
DB_NAME=engage
DB_SSLMODE=disable
```

## Running the Service

### Using Docker Compose (Recommended)

1. Clone the repository
2. Create a `.env` file with your configuration
3. Run the service:
   ```bash
   docker-compose up --build
   ```

The service will be available at `http://localhost:8080`

### Manual Setup

1. Install Go 1.21 or later
2. Install PostgreSQL 16 or later
3. Clone the repository
4. Create a `.env` file with your configuration
5. Build and run:
   ```bash
   go build -o engage ./cmd/engage
   ./engage
   ```

## API Endpoints

### Create an Interaction

```bash
POST /engage
Content-Type: application/json

# For boolean type:
{
  "source": 123,
  "destination": 456,
  "reactionType": "like",
  "value": true
}

# For enum type:
{
  "source": 123,
  "destination": 456,
  "reactionType": "pass",
  "value": "true"
}
```

### Update an Interaction

```bash
PUT /engage
Content-Type: application/json

{
  "source": "user_123",
  "destination": "user_456",
  "reactionType": "pass",
  "value": "false"
}
```

### Delete an Interaction

```bash
DELETE /engage?source=user_123&destination=user_456&reactionType=like
```

### Get Interactions by Source

```bash
GET /engage/source?source=user_123&reactionType=like
```

### Get Interactions by Destination

```bash
GET /engage/destination?destination=user_456&reactionType=pass
```

### Get Interactions by Source List

```bash
GET /engage/sources?sources=123,124,125&reactionType=like
```

### Get Interactions by Destination List

```bash
GET /engage/destinations?destinations=456,457,458&reactionType=visit
```

### Get Interactions Between Source and Destination

```bash
GET /engage/source/destination?source=user_123&destination=user_456
```

### Get Interactions Between Source and Destination List

```bash
POST /engage/source/destinations?source=user_123
Content-Type: application/json

{
  "destinations": ["user_456", "user_789", "user_101"]
}
```

### Get Interactions From Destinations To Source

```bash
POST /engage/destinations/source?source=user_123
Content-Type: application/json

{
  "destinations": ["user_456", "user_789", "user_101"]
}
```

## Performance Considerations

- Uses connection pooling for database connections
- Includes indexes on frequently queried columns
- Supports batch operations for multiple sources/destinations
- Uses efficient JSON parsing and validation

## Adding New Interaction Types

To add new interaction types, modify the `INTERACTION_CONFIG` environment variable. Each interaction type should have:

- `name`: Unique identifier for the interaction
- `type`: Either "boolean" or "enum"
- `options`: Required for enum types, mapping of labels to integer values

Example:
```json
[
  {
    "name": "rating",
    "type": "enum",
    "options": {
      "poor": 1,
      "average": 2,
      "good": 3,
      "excellent": 4
    }
  }
]
```

## Development

### Prerequisites

- Go 1.21+
- PostgreSQL 16+
- Docker and Docker Compose (for containerized deployment)

### Building

```bash
go build -o engage ./cmd/engage
```

### Testing

```bash
go test ./...
```

## License

MIT 