from fastapi import FastAPI
from .temporal_client import ensure_ten_minute_schedule, start_workflow

app = FastAPI(title="Temporal FastAPI Demo", description="A sample FastAPI app with Temporal workflows")


@app.on_event("startup")
async def configure_temporal_schedule() -> None:
    status = await ensure_ten_minute_schedule()
    print(f"Temporal schedule status: {status}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to Temporal FastAPI Demo"}

@app.post("/greet")
async def greet(name: str):
    result = await start_workflow(name)
    return result