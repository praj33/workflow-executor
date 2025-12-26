from typing import Dict, Any


def execute_info(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Informational fetch workflow (read-only).

    Expected payload:
    {
        "action_type": "info",
        "query": "company_holidays"
    }
    """
    query = payload.get("query")

    if not query:
        return {
            "success": False,
            "error": "missing_info_query"
        }

    # Mocked informational response
    return {
        "success": True,
        "query": query,
        "data": f"Mocked information for '{query}'"
    }
