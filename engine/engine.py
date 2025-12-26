from typing import Dict, Any

from workflows.task import execute_task
from workflows.reminder import execute_reminder
from workflows.meeting import execute_meeting
from workflows.info import execute_info


def execute_engine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic execution engine.

    Routes to exactly ONE workflow based on action_type.
    """
    action_type = payload.get("action_type")

    if action_type == "task":
        return execute_task(payload)

    if action_type == "reminder":
        return execute_reminder(payload)

    if action_type == "meeting":
        return execute_meeting(payload)

    if action_type == "info":
        return execute_info(payload)

    return {
        "success": False,
        "error": "unsupported_action_type"
    }
