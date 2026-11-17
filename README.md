# Webhook Processor

A REST API built with **FastAPI** that receives monitoring alerts through webhooks, simulates alert processing, and stores processed alerts in a SQLite database.

## Features

- Receive alerts through a REST API.
- Validate incoming alert data using Pydantic.
- Simulate alert processing with a 3-second delay.
- Store processed alerts in a SQLite database using SQLAlchemy.
- Retrieve stored alerts through a paginated API.
- Run the application using Docker and Docker Compose.
- Persist database data across container restarts.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Docker
- Docker Compose

## Project Structure

```text
webhook-processor/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/mariamreda/webhook-processor.git
cd webhook-processor
```

### 2. Build the Docker image

```bash
docker compose build
```

### 3. Start the application

```bash
docker compose up -d
```

The API will be available at:

`http://localhost:8000`

### 4. Access the API documentation

Open the interactive Swagger documentation:

`http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/webhook` | Receive and process an alert |
| GET | `/alerts` | Retrieve processed alerts with pagination |

### 1. Health Check

**Request:**

```http
GET /health
```

**Response:**

```json
{
  "status": "ok"
}
```

### 2. Receive a Webhook

**Request:**

```http
POST /webhook
```

**Example JSON payload:**

```json
{
  "event_id": "EVT-001",
  "source": "Dynatrace",
  "message": "High CPU utilization detected",
  "timestamp": "2026-11-17T10:30:00"
}
```

The application validates the payload, simulates processing with a 3-second delay, and stores the alert in the database.

**Example response:**

```json
{
  "id": 1,
  "event_id": "EVT-001",
  "source": "Dynatrace",
  "message": "High CPU utilization detected",
  "timestamp": "2026-11-17T10:30:00",
  "status": "processed"
}
```

### 3. Retrieve Processed Alerts

**Request:**

```http
GET /alerts
```

Optional query parameters:

- `skip`: Number of records to skip (default: 0).
- `limit`: Maximum number of records to return (default: 10, maximum: 100).

**Example:**

```http
GET /alerts?skip=0&limit=10
```

The response includes the total number of alerts, pagination information, and the returned alerts.

## Database Persistence

The application uses SQLite to store processed alerts.

Docker Compose mounts a local `data` directory into the container, ensuring that database records remain available after the container is restarted.

## Stopping the Application

```bash
docker compose down
```

The database data is preserved in the mounted `data` directory.

## Author

Mariam Reda