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
from utils.telemetry import emit_execution_event


def execute_engine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic execution engine.

    Required payload fields:
    - trace_id
    - action_type
    """

    trace_id = payload.get("trace_id")
    action_type = payload.get("action_type")
    product = payload.get("product", "unknown")

    # ------------------------------
    # Mandatory guards
    # ------------------------------

    if not trace_id:
        result = {
            "success": False,
            "error_code": "missing_trace_id",
            "message": "trace_id is required for execution",
        }

        emit_execution_event(
            trace_id="unknown",
            action_type=action_type or "unknown",
            adapter="none",
            status="failed",
            product=product,
            error_code="missing_trace_id",
        )

        return result

    if not action_type:
        result = {
            "success": False,
            "trace_id": trace_id,
            "error_code": "missing_action_type",
            "message": "payload.action_type is required",
        }

        emit_execution_event(
            trace_id=trace_id,
            action_type="unknown",
            adapter="none",
            status="failed",
            product=product,
            error_code="missing_action_type",
        )

        return result

    # ------------------------------
    # Adapter resolution
    # ------------------------------

    adapter = get_adapter(action_type)

    if adapter is None:
        result = {
            "success": False,
            "trace_id": trace_id,
            "error_code": "unsupported_action_type",
            "message": f"action_type '{action_type}' is not supported",
        }

        emit_execution_event(
            trace_id=trace_id,
            action_type=action_type,
            adapter="none",
            status="failed",
            product=product,
            error_code="unsupported_action_type",
        )

        return result

    adapter_name = adapter.__class__.__name__

    # ------------------------------
    # Deterministic execution
    # ------------------------------

    try:
        result = adapter.execute(payload)

        # Adapter contract enforcement
        if not isinstance(result, dict) or "success" not in result:
            failure = {
                "success": False,
                "trace_id": trace_id,
                "error_code": "invalid_adapter_response",
                "message": "adapter returned invalid response structure",
            }

            emit_execution_event(
                trace_id=trace_id,
                action_type=action_type,
                adapter=adapter_name,
                status="failed",
                product=product,
                error_code="invalid_adapter_response",
            )

            return failure

        # Telemetry — success or failure (explicit)
        emit_execution_event(
            trace_id=trace_id,
            action_type=action_type,
            adapter=adapter_name,
            status="success" if result.get("success") else "failed",
            product=product,
            error_code=result.get("error_code"),
        )

        # Normalize final output
        return {
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **result,
        }

    except Exception:
        # HARD FAIL — no stack traces, no leaks
        emit_execution_event(
            trace_id=trace_id,
            action_type=action_type,
            adapter=adapter_name,
            status="failed",
            product=product,
            error_code="adapter_execution_failed",
        )

        return {
            "success": False,
            "trace_id": trace_id,
            "error_code": "adapter_execution_failed",
            "message": "execution failed due to internal adapter error",
        }
