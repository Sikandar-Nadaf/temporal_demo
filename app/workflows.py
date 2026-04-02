from datetime import timedelta

from temporalio import workflow
from temporalio.workflow import logger

with workflow.unsafe.imports_passed_through():
    from app.activities import format_greeting, log_heartbeat, send_notification


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> dict:
        logger.info(f"Starting greeting workflow for {name}")

        # Activity 1: format the greeting
        message = await workflow.execute_activity(
            format_greeting,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )

        # Activity 2: send a notification
        notification = await workflow.execute_activity(
            send_notification,
            message,
            start_to_close_timeout=timedelta(seconds=10),
        )

        return {"message": message, "notification": notification}


@workflow.defn
class ScheduledHeartbeatWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # Use workflow.now() to keep workflow execution deterministic.
        now = workflow.now().isoformat()
        logger.info(f"Running scheduled heartbeat at {now}")

        # Activity: persist the heartbeat record
        result = await workflow.execute_activity(
            log_heartbeat,
            now,
            start_to_close_timeout=timedelta(seconds=10),
        )

        return result