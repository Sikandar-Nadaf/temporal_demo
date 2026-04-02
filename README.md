# Temporal FastAPI Demo

This is a sample Python FastAPI project integrated with Temporal for workflow orchestration as an alternative to Celery.

## Prerequisites

- Python 3.10+
- Temporal server running locally

## Installation

1. Clone or download this project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running Temporal Server

This project includes a complete Docker Compose setup with Temporal + PostgreSQL + web UI for development.

### Option 1: Docker Compose (Recommended)

```bash
cp .env.example .env
docker compose up -d
```

This starts all services automatically:
- **Temporal gRPC**: `localhost:7233`
- **Temporal UI**: `http://localhost:3000`
- **PostgreSQL**: `localhost:5432`
- **FastAPI**: `http://localhost:8000` (auto-started)

The stack uses PostgreSQL for Temporal's persistence layer, ensuring workflows and history are durable.

### Option 2: Temporal CLI (Dev Server)

For development without Postgres, you can run:

```bash
temporal server start-dev
```

Then run the app locally outside of Docker.

## Running the Application

### With Docker Compose

Everything runs automatically when you execute `docker compose up -d`.

### Locally (without Compose)

1. Ensure a Temporal server is running (either via Compose or CLI).

2. Set environment variables:
   ```
   cp .env.example .env
   ```

3. Start the Temporal worker:
   ```
   python run_worker.py
   ```

4. In another terminal, start the FastAPI app:
   ```
   python run.py
   ```

## Configuration

### Environment Variables

- `TEMPORAL_ADDRESS`: Temporal server address used by app and worker (default: `localhost:7233`)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: PostgreSQL credentials (default: `temporal`)

### Services

When using Docker Compose, the following services are automatically started:

| Service | URL | Purpose |
|---------|-----|---------|
| Temporal UI | http://localhost:3000 | Web interface for monitoring workflows |
| FastAPI | http://localhost:8000 | REST API for starting workflows |
| Temporal Server | localhost:7233 | gRPC endpoint for workflow execution |
| PostgreSQL | localhost:5432 | Durable storage for workflow history |

### Database

Temporal uses PostgreSQL for persistence:
- Workflow history
- Task metadata
- Namespace configuration
- Visibility records (for search/listing)

The `postgres12` driver is used in the Temporal configuration for PostgreSQL 12+.


## Usage

- GET / : Welcome message
- POST /greet?name=YourName : Starts a Temporal workflow to greet the user
- A Temporal schedule is created at app startup to run a heartbeat workflow every 10 minutes

Example:
```bash
curl -X POST "http://localhost:8000/greet?name=World"
```

Response:
```json
{"message": "Hello, World!"}
```

## Scheduled Task

When the FastAPI app starts, it ensures a Temporal schedule exists with ID `heartbeat-every-10-minutes`.
This schedule triggers `ScheduledHeartbeatWorkflow` every 10 minutes on the same task queue.

## Stopping Services

To stop all running services:

```bash
docker compose down
```

To stop and remove all data (including database volume):

```bash
docker compose down -v
```

## Retention & Archival

By default, Temporal retains closed workflow history for 7 days. After that, execution details are purged from the database.

For long-term audit trails or replay scenarios beyond 7 days, implement archival to cold storage (e.g., S3) or write your own audit logs to a data warehouse.

## Project Structure

- `app/`: FastAPI application code
  - `main.py`: FastAPI app with endpoints
  - `workflows.py`: Temporal workflow definitions
  - `temporal_client.py`: Client to start Temporal workflows
  - `activities.py`: Activities (tasks) executed by workflows
- `worker/`: Temporal worker code
  - `worker.py`: Worker that executes workflows and activities
- `docker-compose.yml`: Container stack (Temporal, Postgres, UI, FastAPI)
- `.env.example`: Environment variable template
- `.gitignore`: Git ignore rules
- `requirements.txt`: Python dependencies
- `run.py`: Script to run FastAPI app locally
- `run_worker.py`: Script to run Temporal worker locally