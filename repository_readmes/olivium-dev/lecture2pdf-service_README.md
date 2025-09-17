# README for olivium-dev/lecture2pdf-service

# Thakii Backend Deployment

This directory contains GitHub Actions workflows and custom actions for deploying the Thakii Lecture2PDF backend service to remote servers using Cloudflare SSH tunnels.

## 🏗️ Architecture

The deployment system consists of:

1. **Custom Cloudflare SSH Action** (`.github/actions/cloudflare-ssh/`)
   - Establishes secure SSH connections through Cloudflare tunnels
   - Handles SSH key setup and configuration
   - Tests connection before proceeding

2. **Deployment Workflow** (`.github/workflows/deploy-to-thakii-02.yml`)
   - Builds and pushes Docker images to GitHub Container Registry
   - Deploys both backend API and worker services
   - Verifies deployment health

## 🚀 Quick Start

### Prerequisites

1. **Server Setup**: Ensure your target server (`thakii-02.fanusdigital.site`) has:
   - Docker and Docker Swarm initialized
   - Cloudflare tunnel configured
   - Firebase service account JSON file at `/home/ec2-user/firebase-service-account.json`

2. **GitHub Secrets**: Configure the following repository secrets:
   ```
   THAKII_02_SSH_PRIVATE_KEY  # Base64 encoded SSH private key
   GITHUB_TOKEN               # Automatically provided by GitHub
   ```

### Deployment

1. Go to **Actions** tab in your GitHub repository
2. Select **"Deploy Thakii Backend to thakii-02"** workflow
3. Click **"Run workflow"** 
4. Configure deployment parameters (or use defaults):
   - Registry: `ghcr.io`
   - Service name: `thakii-lecture2pdf-backend`
   - Internal/External port: `5001`
   - Worker service: `thakii-lecture2pdf-worker`
   - Server: `thakii-02.fanusdigital.site`
   - SSH user: `ec2-user`

## 🔧 Configuration

### Environment Variables

The deployment sets the following environment variables:

```bash
S3_BUCKET_NAME=thakii-video-storage-1753883631
AWS_DEFAULT_REGION=us-east-2
FLASK_ENV=production
PYTHONPATH=/app
```

### Service Configuration

- **Backend Service**: Runs the Flask API on port 5001
- **Worker Service**: Processes video conversion jobs
- **Health Check**: Available at `http://server:5001/health`

### File Mounts

- Firebase service account: `/home/ec2-user/firebase-service-account.json` → `/app/firebase-service-account.json`

## 🔍 Monitoring

After deployment, the workflow automatically:

1. Lists running Docker services
2. Shows recent logs for both services
3. Tests the health endpoint
4. Provides deployment summary with URLs

## 🛠️ Manual Operations

### SSH into Server

```bash
# Using the same Cloudflare tunnel setup
ssh ec2-user@thakii-02.fanusdigital.site
```

### Check Service Status

```bash
# List all services
docker service ls

# Check specific service logs
docker service logs thakii-lecture2pdf-backend
docker service logs thakii-lecture2pdf-worker

# Scale services
docker service scale thakii-lecture2pdf-backend=2
```

### Update Services

```bash
# Update to latest image
docker service update --image ghcr.io/owner/thakii-lecture2pdf-backend:latest thakii-lecture2pdf-backend
```

## 🔐 Security

- SSH connections are secured through Cloudflare tunnels
- Private keys are base64 encoded and stored as GitHub secrets
- Docker images are stored in GitHub Container Registry with authentication
- Services run with restart policies for resilience

## 📊 Service Endpoints

After successful deployment:

- **API**: `http://thakii-02.fanusdigital.site:5001`
- **Health Check**: `http://thakii-02.fanusdigital.site:5001/health`
- **Upload**: `http://thakii-02.fanusdigital.site:5001/upload`

## 🚨 Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   - Verify Cloudflare tunnel is running on the server
   - Check SSH private key is correctly base64 encoded
   - Ensure server hostname is accessible

2. **Docker Service Failed**
   - Check Docker daemon is running: `sudo systemctl status docker`
   - Verify Docker Swarm is initialized: `docker node ls`
   - Check service logs: `docker service logs <service-name>`

3. **Health Check Failed**
   - Verify Firebase service account file exists and is readable
   - Check environment variables are set correctly
   - Review application logs for startup errors

### Debug Commands

```bash
# Check system resources
docker system df
docker system prune

# Inspect service configuration
docker service inspect thakii-lecture2pdf-backend

# Follow logs in real-time
docker service logs -f thakii-lecture2pdf-backend
```

## 📝 Customization

To deploy to a different server:

1. Create a new workflow file (copy `deploy-to-thakii-02.yml`)
2. Update the server hostname and SSH key secret name
3. Adjust service names and ports as needed
4. Configure the new server with required dependencies

## 🔄 Rollback

To rollback to a previous version:

```bash
# Find previous image tag
docker service inspect thakii-lecture2pdf-backend | grep Image

# Update to previous version
docker service update --image ghcr.io/owner/thakii-lecture2pdf-backend:PREVIOUS_TAG thakii-lecture2pdf-backend
```

