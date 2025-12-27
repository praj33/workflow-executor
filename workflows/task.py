from typing import Dict, Any


def execute_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    title = payload.get("title")

    if not title:
        return {
            "success": False,
            "error_code": "missing_task_title",
            "message": "title is required to create a task"
        }

    return {
        "success": True,
        "task_id": "task_001",
        "title": title
    }
