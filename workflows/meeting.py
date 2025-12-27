from typing import Dict, Any


def execute_meeting(payload: Dict[str, Any]) -> Dict[str, Any]:
    title = payload.get("title")
    participants = payload.get("participants")
    start_time = payload.get("start_time")
    end_time = payload.get("end_time")

    if not title or not participants or not start_time or not end_time:
        return {
            "success": False,
            "error_code": "missing_meeting_fields",
            "message": "title, participants, start_time, and end_time are required"
        }

    return {
        "success": True,
        "meeting_id": "meeting_001",
        "title": title,
        "participants": participants,
        "start_time": start_time,
        "end_time": end_time
    }
