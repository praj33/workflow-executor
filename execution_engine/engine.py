"""
PHASE E — REAL WORLD EXECUTION ENGINE (HARDENED)

RESPONSIBILITIES:
- Deterministic adapter routing
- Explicit success / failure
- Zero ambiguity
- Trace-safe execution
- Execute ONLY when action_type is supported

NON-NEGOTIABLES:
- One request → one execution path
- No silent failures
- No exception leakage
"""

from typing import Dict, Any
from datetime import datetime

from adapters.registry import get_adapter


def execute_engine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic execution engine.

    Required payload fields:
    - trace_id
    - action_type
    """

    trace_id = payload.get("trace_id")
    action_type = payload.get("action_type")

    # ------------------------------
    # Mandatory guards
    # ------------------------------

    if not trace_id:
        return {
            "success": False,
            "error_code": "missing_trace_id",
            "message": "trace_id is required for execution",
        }

    if not action_type:
        return {
            "success": False,
            "trace_id": trace_id,
            "error_code": "missing_action_type",
            "message": "payload.action_type is required",
        }

    # ------------------------------
    # Adapter resolution
    # ------------------------------

    adapter = get_adapter(action_type)

    if adapter is None:
        return {
            "success": False,
            "trace_id": trace_id,
            "error_code": "unsupported_action_type",
            "message": f"action_type '{action_type}' is not supported",
        }

    # ------------------------------
    # Deterministic execution
    # ------------------------------

    try:
        result = adapter.execute(payload)

        # Adapter contract enforcement
        if not isinstance(result, dict) or "success" not in result:
            return {
                "success": False,
                "trace_id": trace_id,
                "error_code": "invalid_adapter_response",
                "message": "adapter returned invalid response structure",
            }

        # Normalize final output
        return {
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat(),
            **result,
        }

    except Exception:
        # HARD FAIL — no stack traces, no leaks
        return {
            "success": False,
            "trace_id": trace_id,
            "error_code": "adapter_execution_failed",
            "message": "execution failed due to internal adapter error",
        }
