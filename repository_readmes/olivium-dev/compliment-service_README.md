# README for olivium-dev/compliment-service

# Compliment Service

A FastAPI-based microservice for managing compliments between users. This service allows users to send compliments to each other and view their conversation history.

## Features

- Send compliments between users
- View all users you've exchanged compliments with
- View all users who have sent you compliments
- View conversation history between two users
- RESTful API with proper error handling
- PostgreSQL database integration
- Swagger UI documentation

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn
- Docker

## Prerequisites

- Python 3.13 or higher
- PostgreSQL database
- pip (Python package manager)
- Docker (optional)

## Installation

### Standard Installation

1. Clone the repository:
```bash
git clone https://github.com/olivium-dev/compliment-service.git
cd compliment-service
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

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/compliment_db
```

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/olivium-dev/compliment-service.git
cd compliment-service
```

2. Build the Docker image:
```bash
docker build -t compliment-service .
```

3. Run the container:
```bash
docker run -d -p 6070:6070 --name compliment-service-container \
  -e DATABASE_URL=postgresql://username:password@host.docker.internal:5432/compliment_db \
  compliment-service
```

Note: Use `host.docker.internal` to connect to PostgreSQL running on your host machine from within the container.

## Running the Service

### Standard Method
```bash
uvicorn main:app --reload --port 6070
```

### Using Docker
```bash
# The service is already running if you started the container as shown above
# To check the logs:
docker logs -f compliment-service-container

# To stop the service:
docker stop compliment-service-container

# To start it again:
docker start compliment-service-container
```

Access the API documentation:
- Swagger UI: http://localhost:6070/docs
- ReDoc: http://localhost:6070/redoc

## API Endpoints

### Create a Compliment
```bash
POST /api/v1/compliments/
```
Request body:
```json
{
    "partner_id_1": "user_123",
    "partner_id_2": "user_456",
    "message": "You're amazing!"
}
```

### Get All Users You've Exchanged With
```bash
GET /api/v1/compliments/users?user_id=user_123
```

### Get All Users Who Sent You Compliments
```bash
GET /api/v1/compliments/received?user_id=user_123
```

### Get Conversation History
```bash
GET /api/v1/compliments/conversation?user_id_1=user_123&user_id_2=user_456
```

## Response Examples

### Conversation Response
```json
{
    "user_id_1": "user_123",
    "user_id_2": "user_456",
    "total_messages": 3,
    "first_message_date": "2025-05-01T22:59:23.510123",
    "last_message_date": "2025-05-02T20:48:53.177603",
    "messages": [
        {
            "content": "You're amazing!",
            "timestamp": "2025-05-01T22:59:23.510123"
        },
        {
            "content": "Thank you! You're great too!",
            "timestamp": "2025-05-01T22:59:27.920835"
        }
    ]
}
```

## Development

### Project Structure
```
compliment-service/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── database.py
│   ├── endpoints/
│   │   └── compliment.py
│   ├── models/
│   │   └── compliment.py
│   └── schemas/
│       ├── compliment.py
│       └── conversation.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### Running Tests
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue in the repository. 