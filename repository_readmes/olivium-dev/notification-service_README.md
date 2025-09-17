# README for olivium-dev/notification-service

# Notification Service

A FastAPI-based microservice for managing various types of notifications with MongoDB backend.

## Features

- Dynamic notification types based on configuration
- MongoDB integration for data persistence
- Docker support for easy deployment
- RESTful API endpoints for:
  - Creating notifications (order, user, system)
  - Retrieving notifications
  - Updating notification status
  - Deactivating notifications
  - Filtering and pagination support

## Setup

### Prerequisites
- Python 3.11+
- MongoDB
- Docker (optional)

### Environment Variables
Create a `.env` file with:
```
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_CLUSTER=your_cluster
MONGODB_DATABASE=your_database
```

### Running Locally
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Running with Docker
1. Build the image:
```bash
docker build -t notification-service .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 --name notification-service-container notification-service
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Notification types are configured in `notification_config.json`. Add new notification types by extending this configuration file. 

## API Endpoints

### Notification Management

#### Single Notification Operations
- `PATCH /notifications/{notification_id}/mark-read` - Mark a single notification as read
- `PATCH /notifications/{notification_id}/mark-unread` - Mark a single notification as unread
- `PATCH /notifications/{notification_id}/deactivate` - Deactivate a single notification (soft delete)
- `PATCH /notifications/{notification_id}/reactivate` - Reactivate a single deactivated notification
- `PATCH /notifications/{notification_id}/status` - Update notification status to any valid value
- `PATCH /notifications/{notification_id}` - Update notification content (title, subtitle, description)

#### Bulk Operations
- `PATCH /notifications/bulk/mark-read` - Mark multiple notifications as read
- `PATCH /notifications/bulk/mark-unread` - Mark multiple notifications as unread
- `PATCH /notifications/bulk/deactivate` - Deactivate multiple notifications (soft delete)
- `PATCH /notifications/bulk/reactivate` - Reactivate multiple deactivated notifications

#### Receiver Operations
- `PATCH /notifications/receiver/{receiver_id}/mark-all-read` - Mark all notifications as read for a specific receiver 