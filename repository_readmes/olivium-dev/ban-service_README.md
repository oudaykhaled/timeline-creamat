# README for olivium-dev/ban-service

# Ban Service

A comprehensive ban management microservice built with Rust, featuring dynamic ban rules, Redis storage, and progressive ban enforcement.

## Features

- **Dynamic Ban Rules**: JSON-configurable ban rules with hot-reloading
- **Progressive Ban System**: Multi-stage bans (WARNING → PARTIAL_BAN → BAN)
- **Two Ban Types**: Yellow (3 stages) and Red (2 stages) ban progressions
- **Redis Integration**: Fast, persistent storage with TTL support
- **Comprehensive API**: RESTful endpoints for ban management
- **Health Monitoring**: Built-in health check endpoints
- **Production Ready**: Docker support, logging, and error handling
- **Interactive API Documentation**: Full Swagger UI integration
- **Docker Swarm Deployment**: Automated deployment with GitHub Actions
- **Comprehensive Testing**: Complete Postman collection with automated tests

## Ban System Overview

The ban service implements a progressive ban system with two types of bans:

- **Yellow Ban**: 3 stages (WARNING → PARTIAL_BAN → BAN)
- **Red Ban**: 2 stages (PARTIAL_BAN → BAN)

### Ban Types

- **WARNING**: User receives a warning with no functional restrictions
- **PARTIAL_BAN**: User is temporarily banned for a specified duration
- **BAN**: User is permanently banned

## API Documentation

### Interactive Swagger UI

Once the service is running, you can access the interactive Swagger UI documentation at:

```
http://localhost:3000/swagger-ui/
```

The Swagger UI provides:
- **Complete API Documentation**: All endpoints with detailed descriptions
- **Interactive Testing**: Test API calls directly from the browser
- **Request/Response Examples**: See exactly what data to send and expect
- **Schema Documentation**: Detailed information about all data models
- **Error Code Reference**: Complete list of possible error responses

### OpenAPI Specification

The OpenAPI 3.1 specification is available at:

```
http://localhost:3000/api-docs/openapi.json
```

You can use this specification with:
- **Code Generation**: Generate client libraries in various languages
- **API Testing Tools**: Import into Postman, Insomnia, or similar tools
- **Documentation Tools**: Generate static documentation
- **Validation Tools**: Validate API requests and responses

## Configuration

### Ban Rules Configuration

Ban rules are configured in `config/banning-rule.json`:

```json
{
  "BanTypes": {
    "yellow": {
      "1": {
        "type": "WARNING",
        "message": "Label{{Ban.Label.YOU_WILL_BE_BANNED_AFTER_ONE_WARNING}}"
      },
      "2": {
        "type": "PARTIAL_BAN",
        "message": "Label{{Ban.Label.YOU_ARE_BANNED_FOR_1_HOUR}}",
        "bannedForXMinutes": 60
      },
      "3": {
        "type": "BAN",
        "message": "Label{{Ban.Label.YOU_ARE_BANNED}}"
      }
    },
    "red": {
      "1": {
        "type": "PARTIAL_BAN",
        "message": "Label{{Ban.Label.YOU_ARE_BANNED_FOR_3_DAYS}}",
        "bannedForXMinutes": 4320
      },
      "2": {
        "type": "BAN",
        "message": "Label{{Ban.Label.YOU_ARE_BANNED}}"
      }
    }
  }
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RUST_LOG` | `info` | Log level |
| `REDIS_URL` | `redis://127.0.0.1:6379` | Redis connection URL |
| `SERVER_HOST` | `127.0.0.1` | Server bind address |
| `SERVER_PORT` | `3000` | Server port |
| `BAN_RULES_FILE` | `./config/banning-rule.json` | Path to ban rules file |

## API Endpoints

### 1. Apply Ban
```http
POST /api/v1/ban/{uuid}/{ban_type}
```

Applies a ban to a user based on the current stage and ban type rules.

**Example:**
```bash
curl -X POST http://localhost:3000/api/v1/ban/123e4567-e89b-12d3-a456-426614174000/yellow
```

**Response:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "ban_type": "yellow",
  "current_stage": 1,
  "status": "WARNING",
  "message": "Label{{Ban.Label.YOU_WILL_BE_BANNED_AFTER_ONE_WARNING}}",
  "banned_until": null,
  "last_updated": "2024-01-01T12:00:00Z",
  "is_currently_banned": false
}
```

### 2. Get Ban Status
```http
GET /api/v1/ban/{uuid}/status
```

Returns the current ban status for a user across all ban types.

**Example:**
```bash
curl http://localhost:3000/api/v1/ban/123e4567-e89b-12d3-a456-426614174000/status
```

**Response:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "ban_statuses": [
    {
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "ban_type": "yellow",
      "current_stage": 2,
      "status": "PARTIAL_BAN",
      "message": "Label{{Ban.Label.YOU_ARE_BANNED_FOR_1_HOUR}}",
      "banned_until": "2024-01-01T13:00:00Z",
      "last_updated": "2024-01-01T12:00:00Z",
      "is_currently_banned": true
    }
  ]
}
```

### 3. Update Ban Status
```http
POST /api/v1/ban/{uuid}/update
```

Checks for expired bans and updates the status accordingly.

**Example:**
```bash
curl -X POST http://localhost:3000/api/v1/ban/123e4567-e89b-12d3-a456-426614174000/update
```

**Response:**
```json
{
  "old_status": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "ban_type": "yellow",
    "current_stage": 2,
    "status": "PARTIAL_BAN",
    "message": "Label{{Ban.Label.YOU_ARE_BANNED_FOR_1_HOUR}}",
    "banned_until": "2024-01-01T13:00:00Z",
    "last_updated": "2024-01-01T12:00:00Z",
    "is_currently_banned": false
  },
  "new_status": null,
  "updated": true
}
```

### 4. Force Reset Ban Status
```http
POST /api/v1/ban/{uuid}/force-reset
```

Completely resets all ban statuses for a user.

**Example:**
```bash
curl -X POST http://localhost:3000/api/v1/ban/123e4567-e89b-12d3-a456-426614174000/force-reset
```

**Response:**
```json
{
  "old_status": {
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "ban_type": "yellow",
    "current_stage": 2,
    "status": "PARTIAL_BAN",
    "message": "Label{{Ban.Label.YOU_ARE_BANNED_FOR_1_HOUR}}",
    "banned_until": "2024-01-01T13:00:00Z",
    "last_updated": "2024-01-01T12:00:00Z",
    "is_currently_banned": true
  },
  "new_status": null,
  "updated": true
}
```

### 5. Health Check
```http
GET /health
```

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "ban-service",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## API Testing

### Postman Collections

The project includes comprehensive Postman collections for testing all API scenarios:

- **Collection**: `postman/Ban-Service-Collection.json`
- **Environment**: `postman/Ban-Service-Environment.json`
- **Documentation**: `postman/README.md`

#### Features
- **Complete Test Coverage**: All endpoints with various scenarios
- **Ban Progression Testing**: Step-by-step ban stage progression
- **Error Scenario Testing**: Invalid inputs and edge cases
- **Performance Testing**: Response time validation
- **Automated Cleanup**: Reset test data after testing

#### Quick Start
```bash
# Install Newman (Postman CLI)
npm install -g newman

# Run all tests
cd postman
./run-tests.sh all

# Run specific test types
./run-tests.sh smoke      # Health check and basic functionality
./run-tests.sh performance # Performance tests
./run-tests.sh error      # Error scenarios
./run-tests.sh load 50    # Load testing with 50 iterations
```

#### Import to Postman
1. Open Postman
2. Click "Import"
3. Select `postman/Ban-Service-Collection.json` and `postman/Ban-Service-Environment.json`
4. Select "Ban Service Environment" from the environment dropdown
5. Update the `baseUrl` variable to match your service URL
6. Run individual tests or the entire collection

#### Test Categories
- **Health Check**: Service availability and health
- **Yellow Ban Progression**: 3-stage ban system testing
- **Red Ban Progression**: 2-stage ban system testing
- **Ban Status Management**: Status retrieval and updates
- **Error Scenarios**: Invalid UUID, ban types, etc.
- **Edge Cases**: Multiple ban types, beyond max stage
- **Performance Tests**: Response time validation
- **Cleanup**: Test data cleanup utilities

#### Automated Testing
```bash
# Run tests with detailed reporting
newman run postman/Ban-Service-Collection.json \
  -e postman/Ban-Service-Environment.json \
  --reporters cli,html \
  --reporter-html-export test-report.html

# Run specific test folder
newman run postman/Ban-Service-Collection.json \
  -e postman/Ban-Service-Environment.json \
  --folder "Yellow Ban Progression"
```

## Deployment

### Prerequisites

- **Rust** (1.72+)
- **Redis** (6.0+)
- **Docker** (for containerized deployment)
- **Docker Swarm** (for production deployment)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ban-service
   ```

2. **Install Redis:**
   ```bash
   # macOS
   brew install redis
   brew services start redis
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install redis-server
   sudo systemctl start redis-server
   
   # Docker
   docker run -d -p 6379:6379 redis:7-alpine
   ```

3. **Set up environment:**
   ```bash
   export REDIS_URL=redis://127.0.0.1:6379
   export SERVER_HOST=127.0.0.1
   export SERVER_PORT=3000
   export BAN_RULES_FILE=./config/banning-rule.json
   ```

4. **Install dependencies and run:**
   ```bash
   cargo build
   cargo run
   ```

5. **Access the service:**
   - **API**: http://localhost:3000
   - **Swagger UI**: http://localhost:3000/swagger-ui/
   - **Health Check**: http://localhost:3000/health

### Docker Swarm Deployment

The service includes automated deployment using GitHub Actions with Docker Swarm.

#### GitHub Actions Workflow

The deployment workflow (`.github/workflows/deploy.yml`) provides:

- **Multi-architecture builds**: Supports both AMD64 and ARM64
- **Automated Redis setup**: Creates Redis service with persistence
- **Zero-downtime deployment**: Rolling updates with Docker Swarm
- **Configurable parameters**: All deployment parameters can be customized

#### Deployment Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `registry` | `ghcr.io` | Docker registry URL |
| `service_name` | `ban-service` | Service name for deployment |
| `internal_port` | `3000` | Internal port of the service |
| `external_port` | `10042` | External port for access |
| `server` | `ec2-user@ec2-3-147-11-27.us-east-2.compute.amazonaws.com` | SSH server address |
| `ssh_option` | `swt` | SSH key option (swt or swg) |

#### Required GitHub Secrets

- `SWT_SSH_PRIVATE_KEY`: Base64-encoded SSH private key for SWT option
- `SWG_SSH_PRIVATE_KEY`: Base64-encoded SSH private key for SWG option
- `GITHUB_TOKEN`: GitHub token for registry access (automatically provided)

#### Manual Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t ban-service .
   ```

2. **Run Redis service:**
   ```bash
   docker service create \
     --name ban-service-redis \
     --publish published=6379,target=6379 \
     --mount type=volume,source=redis-data,destination=/data \
     --replicas 1 \
     redis:latest redis-server --appendonly yes
   ```

3. **Run the ban service:**
   ```bash
   docker service create \
     --name ban-service \
     --publish published=3000,target=3000 \
     --replicas 1 \
     --env REDIS_URL=redis://redis:6379 \
     --env SERVER_HOST=0.0.0.0 \
     --env SERVER_PORT=3000 \
     ban-service
   ```

## Development

### Running Tests

```bash
# Run all tests
cargo test

# Run with logging
RUST_LOG=debug cargo test

# Run specific test
cargo test test_ban_rules
```

### Code Generation from OpenAPI

The service includes comprehensive OpenAPI 3.1 specification. You can generate client libraries:

```bash
# Generate TypeScript client
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:3000/api-docs/openapi.json \
  -g typescript-fetch \
  -o ./clients/typescript

# Generate Python client
openapi-generator-cli generate \
  -i http://localhost:3000/api-docs/openapi.json \
  -g python \
  -o ./clients/python
```

### API Testing with Swagger UI

1. **Start the service**: `cargo run`
2. **Open Swagger UI**: http://localhost:3000/swagger-ui/
3. **Explore the API**: Browse all available endpoints
4. **Test endpoints**: Use the "Try it out" button on any endpoint
5. **View responses**: See real API responses and error codes

## Monitoring and Observability

### Logging

The service uses structured logging with configurable levels:

```bash
# Set log level
export RUST_LOG=debug
cargo run

# JSON logging for production
export RUST_LOG=info
cargo run
```

### Health Checks

- **Endpoint**: `GET /health`
- **Purpose**: Service and dependency health monitoring
- **Response**: JSON with service status and timestamp

### Metrics

The service is designed to be easily integrated with monitoring solutions:

- Structured logs for log aggregation
- Health check endpoints for uptime monitoring
- Error responses with proper HTTP status codes

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Swagger UI    │    │   API Gateway   │    │   Load Balancer │
│   (Optional)    │    │   (Optional)    │    │   (Optional)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                 ┌─────────────────────────────┐
                 │       Ban Service           │
                 │  ┌─────────────────────┐   │
                 │  │   REST API          │   │
                 │  │   (Actix-Web)       │   │
                 │  └─────────────────────┘   │
                 │  ┌─────────────────────┐   │
                 │  │   Business Logic    │   │
                 │  │   (Ban Rules)       │   │
                 │  └─────────────────────┘   │
                 │  ┌─────────────────────┐   │
                 │  │   Redis Client      │   │
                 │  │   (Connection Pool) │   │
                 │  └─────────────────────┘   │
                 └─────────────────────────────┘
                                 │
                 ┌─────────────────────────────┐
                 │       Redis Store           │
                 │   ┌─────────────────────┐   │
                 │   │   Ban Status Data   │   │
                 │   │   (TTL Support)     │   │
                 │   └─────────────────────┘   │
                 └─────────────────────────────┘
```

## Performance

### Benchmarks

The service is designed for high performance:

- **Async Runtime**: Tokio-based async processing
- **Connection Pooling**: Redis connection pooling
- **Efficient Serialization**: Fast JSON processing
- **Memory Management**: Rust's zero-cost abstractions

### Scaling

- **Horizontal**: Multiple service instances with Docker Swarm
- **Vertical**: Increased CPU/memory per instance
- **Database**: Redis clustering for larger datasets
- **Caching**: Built-in Redis caching with TTL

## Security

### Authentication

The service currently doesn't include authentication. For production deployment, consider:

- **API Gateway**: Use an API gateway for authentication
- **JWT Tokens**: Implement JWT token validation
- **Rate Limiting**: Add rate limiting to prevent abuse
- **HTTPS**: Always use HTTPS in production

### Input Validation

- **UUID Validation**: All user IDs must be valid UUIDs
- **Ban Type Validation**: Only configured ban types are accepted
- **Request Validation**: All requests are validated against schemas

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests**: Ensure your changes are tested
5. **Update documentation**: Update API docs if needed
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: Check the Swagger UI at http://localhost:3000/swagger-ui/
- **Issues**: Report issues on the GitHub issue tracker
- **API Questions**: Use the interactive Swagger UI for API exploration
- **Testing**: Use the comprehensive Postman collections in the `postman/` directory 