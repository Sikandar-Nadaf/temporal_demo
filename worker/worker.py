import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from app.activities import format_greeting, log_heartbeat, send_notification
from app.workflows import GreetingWorkflow, ScheduledHeartbeatWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="greeting-tasks",
        workflows=[GreetingWorkflow, ScheduledHeartbeatWorkflow],
        activities=[format_greeting, send_notification, log_heartbeat],
    )
    print("Starting Temporal worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())