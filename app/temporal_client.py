import os
from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleAlreadyRunningError,
    ScheduleIntervalSpec,
    ScheduleSpec,
)
from temporalio.service import RPCError, RPCStatusCode

from .workflows import GreetingWorkflow, ScheduledHeartbeatWorkflow

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TASK_QUEUE = "greeting-tasks"
SCHEDULE_ID = "heartbeat-every-10-minutes"


async def get_client() -> Client:
    return await Client.connect(TEMPORAL_ADDRESS)

async def start_workflow(name: str):
    client = await get_client()
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        name,
        id=f"greeting-workflow-{name}",
        task_queue=TASK_QUEUE,
    )
    return result


async def ensure_ten_minute_schedule() -> str:
    client = await get_client()
    schedule = Schedule(
        action=ScheduleActionStartWorkflow(
            ScheduledHeartbeatWorkflow.run,
            id="scheduled-heartbeat-workflow",
            task_queue=TASK_QUEUE,
        ),
        spec=ScheduleSpec(intervals=[ScheduleIntervalSpec(every=timedelta(minutes=10))]),
    )

    try:
        await client.create_schedule(SCHEDULE_ID, schedule)
        return "created"
    except (ScheduleAlreadyRunningError, RPCError) as err:
        if isinstance(err, ScheduleAlreadyRunningError) or (
            isinstance(err, RPCError) and err.status == RPCStatusCode.ALREADY_EXISTS
        ):
            return "already-exists"
        raise