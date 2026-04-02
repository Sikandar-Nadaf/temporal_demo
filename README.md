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

For development, this project includes a Docker Compose setup with Temporal + PostgreSQL:

```bash
cp .env.example .env
docker compose up -d
```

Temporal gRPC endpoint: `localhost:7233`
Temporal UI: `http://localhost:8233`

If you prefer Temporal CLI dev server without Postgres, you can still run:

```bash
temporal server start-dev
```

## Running the Application

1. Ensure environment variables are available:

   ```
   cp .env.example .env
   ```

2. Start the Temporal worker:

   ```
   python run_worker.py
   ```

3. In another terminal, start the FastAPI app:

   ```
   python run.py
   ```

4. The API will be available at http://localhost:8000

## Configuration

- `TEMPORAL_ADDRESS`: Temporal server address used by app and worker (default: `localhost:7233`)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: used by Docker Compose services


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

## Project Structure

- `app/`: FastAPI application code
  - `main.py`: FastAPI app with endpoints
  - `workflows.py`: Temporal workflow definitions
  - `temporal_client.py`: Client to start Temporal workflows
- `worker/`: Temporal worker code
  - `worker.py`: Worker that executes workflows
- `requirements.txt`: Python dependencies
- `run.py`: Script to run FastAPI app
- `run_worker.py`: Script to run Temporal worker