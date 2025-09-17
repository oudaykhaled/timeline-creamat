# README for olivium-dev/server-saawt-config

# SAAWT Server Configuration

This repository contains configuration files for the SAAWT server infrastructure.

## Components

- **nginx**: Web server configuration for reverse proxying to various services
- **static-pages**: Static HTML pages served directly by nginx

## Services

The following services are available:

- Main website: [saawtcloud.net](https://saawtcloud.net)
- Gateway: [saawtcloud.net/gateway](https://saawtcloud.net/gateway)
- User Management: [saawtcloud.net/user](https://saawtcloud.net/user)
- Log Service: [log.saawtcloud.net](https://log.saawtcloud.net)
- **Support Page: [saawtcloud.net/static-pages/support](https://saawtcloud.net/static-pages/support)**

## Static Pages

The repository now includes a static pages system for serving HTML content directly through nginx:

### Available Pages

- **Support Page** (`/static-pages/support`): Customer support page with WhatsApp integration
  - Contact number: +972 59-884-1158
  - Dark theme design matching SAAWT branding
  - Responsive mobile-friendly interface

### Adding New Static Pages

1. Create HTML files in the `static-pages/` directory
2. Commit and push changes to automatically trigger deployment
3. Pages are accessible at `https://saawtcloud.net/static-pages/[filename]`

## Log Service

The log service is available at [log.saawtcloud.net](https://log.saawtcloud.net) and provides the following functionality:

- Web interface for viewing logs (Frontend port: 10101)
- RESTful API for log management (Backend port: 10100)
- Upload logs via HTTP POST to `log.saawtcloud.net/upload`
- Direct access to log files at `log.saawtcloud.net/logs`
- Health check endpoint at `log.saawtcloud.net/health`

### Port Configuration

The log service runs on the following ports:

- Backend service: 10100 (internal) - Handles API requests and log processing
- Frontend UI: 10101 (internal) - Provides web interface for log viewing

These port numbers are defined in the GitHub Actions deployment workflow.

### Setting up the Log Service

To set up the log service, run the setup script:

```bash
./setup-log-service.sh
```

This script will:
1. Create the log directory at `/var/log/saawt`
2. Set appropriate permissions
3. Create a test log file
4. Check if services are running on the expected ports
5. Reload the nginx configuration

## Deployment

### Static Pages Deployment

Static pages are automatically deployed using the "Deploy Static Pages" GitHub Actions workflow when:
- Changes are pushed to the `main` branch in the `static-pages/` directory
- Nginx configuration changes are made
- Manual deployment can be triggered via the GitHub Actions interface

### Log Service Deployment

The log service is deployed using GitHub Actions workflow. The workflow:

1. Builds and pushes the Docker image to GitHub Container Registry
2. Deploys the image to the EC2 instance
3. Maps the container ports (8080 for backend and 4200 for frontend) to the server ports (10100 and 10101)

## Configuration Updates

When making changes to the configuration files, remember to:

1. Test the configuration with `nginx -t`
2. Reload nginx with `systemctl reload nginx`
3. Verify the service is accessible at the appropriate domain
4. For static pages: Verify accessibility at `https://saawtcloud.net/static-pages/[page-name]`