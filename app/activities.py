import logging
from datetime import datetime

from temporalio import activity

logger = logging.getLogger(__name__)


@activity.defn
async def format_greeting(name: str) -> str:
    """Format a personalised greeting string."""
    logger.info("format_greeting: name=%s", name)
    return f"Hello, {name}! Welcome to Temporal."


@activity.defn
async def send_notification(message: str) -> dict:
    """Simulate sending a notification (e.g. email / push / Slack)."""
    logger.info("send_notification: %s", message)
    # In a real project, call your email/SMS/webhook service here.
    return {"status": "sent", "message": message, "sent_at": datetime.utcnow().isoformat()}


@activity.defn
async def log_heartbeat(timestamp: str) -> dict:
    """Persist a scheduled-heartbeat record (e.g. to a DB or monitoring system)."""
    logger.info("log_heartbeat: timestamp=%s", timestamp)
    # In a real project, write to a DB or push a metric here.
    return {"status": "logged", "timestamp": timestamp}
