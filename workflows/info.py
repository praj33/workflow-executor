from typing import Dict, Any


def execute_info(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query")

    if not query:
        return {
            "success": False,
            "error_code": "missing_info_query",
            "message": "query is required for informational fetch"
        }

    return {
        "success": True,
        "query": query,
        "data": f"Mocked information for '{query}'"
    }
