"""
PHASE C — EXECUTION ENGINE (DAY 3 HARDENED)

RESPONSIBILITIES:
- Deterministic routing
- Explicit success / failure
- Zero ambiguity

FAILURE RULES:
- All failures must include an error_code
- No silent fallbacks
- Unsupported paths must fail explicitly
"""

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

    if not action_type:
        return {
            "success": False,
            "error_code": "missing_action_type",
            "message": "payload.action_type is required"
        }

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
        "error_code": "unsupported_action_type",
        "message": f"action_type '{action_type}' is not supported"
    }
