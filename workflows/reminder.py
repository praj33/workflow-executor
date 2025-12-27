from typing import Dict, Any


def execute_reminder(payload: Dict[str, Any]) -> Dict[str, Any]:
    message = payload.get("message")
    time = payload.get("time")

    if not message or not time:
        return {
            "success": False,
            "error_code": "missing_reminder_fields",
            "message": "message and time are required"
        }

    return {
        "success": True,
        "reminder_id": "reminder_001",
        "message": message,
        "time": time
    }
