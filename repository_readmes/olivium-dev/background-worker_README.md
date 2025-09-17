# README for olivium-dev/background-worker

# REST Jobs Microservice

A production-ready Go microservice for executing scheduled HTTP requests (jobs) with advanced monitoring, retry logic, and observability features.

## 🚀 Features

- **Cron-based Scheduling**: Execute jobs on precise schedules (seconds, minutes, hours, days)
- **HTTP Request Execution**: Parse and execute curl commands from template files
- **Retry Logic**: Configurable retry attempts with exponential backoff
- **Concurrency Control**: Limit concurrent job executions
- **Database Persistence**: Track job executions and statistics with PostgreSQL
- **Monitoring & Metrics**: Prometheus metrics and health checks
- **RESTful API**: Comprehensive API for job management and monitoring
- **Template Support**: Go templates in curl files for dynamic values
- **Environment Variable Substitution**: Secure configuration management
- **Graceful Shutdown**: Clean shutdown with proper resource cleanup
- **Docker Support**: Containerized deployment with Docker Compose

## 📁 Project Structure

```
rest-jobs-microservice/
├── cmd/
│   └── main.go                 # Application entry point
├── internal/
│   ├── api/                    # REST API handlers and server
│   ├── config/                 # Configuration management
│   ├── database/               # Database connection and migrations
│   ├── scheduler/              # Job scheduling and management
│   ├── executor/               # Job execution engine
│   └── models/                 # Database models
├── pkg/
│   ├── logger/                 # Structured logging
│   └── metrics/                # Prometheus metrics
├── jobs/                       # Curl template files
├── config.json                 # Microservice configuration
├── jobs.json                   # Job definitions
├── docker-compose.yml          # Docker Compose setup
├── Dockerfile                  # Container build
└── Makefile                    # Build automation
```

## 🛠 Quick Start

### Prerequisites

- Go 1.21+
- PostgreSQL 12+
- Docker & Docker Compose (for containerized setup)

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd rest-jobs-microservice
   make init
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

3. **Start PostgreSQL**
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_DB=rest_jobs_db \
     -e POSTGRES_USER=rest_jobs_user \
     -e POSTGRES_PASSWORD=rest_jobs_pass \
     -p 5432:5432 postgres:15-alpine
   ```

4. **Run the Service**
   ```bash
   make run
   ```

### Docker Deployment

```bash
# Start all services (PostgreSQL + Microservice + Prometheus)
docker-compose up -d

# View logs
docker-compose logs -f rest-jobs-microservice

# Stop services
docker-compose down
```

## 📖 Configuration

### Job Configuration (`jobs.json`)

```json
[
    {
        "name": "api-health-check",
        "description": "Check API health every 5 minutes",
        "curl-file": "health-check.curlx",
        "run-every": "5m",
        "enabled": true,
        "timeout": "10s",
        "retry-count": 2,
        "retry-delay": "30s"
    }
]
```

### Curl Templates (`jobs/*.curlx`)

```bash
curl -X GET "https://api.example.com/health" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "User-Agent: RestJobsMicroservice/1.0" \
  -d '{
    "timestamp": "{{.Now.UTC.Format \"2006-01-02T15:04:05Z\"}}",
    "source": "microservice"
  }' \
  --connect-timeout 5 \
  --max-time 10
```

### Scheduling Formats

- `30s` - Every 30 seconds
- `5m` - Every 5 minutes  
- `2h` - Every 2 hours
- `1d` - Every day

## 🔌 API Endpoints

### Health & Status
- `GET /health` - Service health check
- `GET /` - Service information
- `GET /metrics` - Prometheus metrics

### Job Management
- `GET /api/v1/jobs/stats` - All job statistics
- `GET /api/v1/jobs/stats/{jobName}` - Specific job stats
- `GET /api/v1/jobs/executions` - Job execution history
- `GET /api/v1/jobs/executions/{id}` - Execution details
- `POST /api/v1/jobs/executions/{id}/cancel` - Cancel running job

### System Monitoring
- `GET /api/v1/system/status` - System status and metrics

## 📊 Monitoring

### Prometheus Metrics

- `rest_jobs_executions_total` - Total job executions by status
- `rest_jobs_execution_duration_seconds` - Job execution duration
- `rest_jobs_active` - Currently active jobs
- `rest_jobs_scheduled` - Number of scheduled jobs
- `rest_jobs_http_requests_total` - HTTP requests made by jobs

### Health Checks

The service provides comprehensive health checks:
- Database connectivity
- System uptime
- Active job count
- Recent failure rates

## 🔄 Job Lifecycle

1. **Scheduling**: Jobs are scheduled based on `run-every` configuration
2. **Execution**: HTTP requests are executed via curl templates
3. **Recording**: Results are stored in PostgreSQL
4. **Retry Logic**: Failed jobs are retried according to configuration
5. **Metrics**: Performance metrics are recorded for monitoring

## 🛡 Security Features

- Environment variable substitution for sensitive data
- Configurable timeouts and limits
- Rate limiting support
- Secure headers in HTTP requests
- Input validation and sanitization

## 🚀 Production Deployment

### Environment Variables

```bash
# Database
DB_HOST=your-db-host
DB_NAME=rest_jobs_db
DB_USER=rest_jobs_user
DB_PASSWORD=secure-password

# API Tokens (for job authentication)
API_TOKEN=your-api-token
BACKUP_API_TOKEN=backup-token

# Service Configuration
PORT=8080
ENVIRONMENT=production
LOG_LEVEL=info
LOG_FORMAT=json
```

### Docker Production Build

```bash
# Build production image
make build-prod
docker build -t rest-jobs-microservice:latest .

# Deploy with production compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```bash
# Run unit tests
make test

# Test individual components
go test ./internal/executor/...
go test ./internal/scheduler/...

# Integration tests
go test -tags integration ./...
```

## 📈 Performance

- **Concurrent Jobs**: Configurable limit (default: 10)
- **Database Pool**: Optimized connection pooling
- **Memory Usage**: Efficient execution tracking
- **HTTP Timeouts**: Configurable per job
- **Retry Strategy**: Exponential backoff

## 🔧 Development

### Adding New Jobs

1. Create curl template in `jobs/` directory
2. Add job configuration to `jobs.json`
3. Restart service or reload configuration

### Custom Metrics

Add custom Prometheus metrics in `pkg/metrics/metrics.go`:

```go
var CustomMetric = promauto.NewCounterVec(
    prometheus.CounterOpts{
        Name: "custom_metric_total",
        Help: "Description of custom metric",
    },
    []string{"label1", "label2"},
)
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the logs for debugging information

---

**Built with ❤️ in Go**
