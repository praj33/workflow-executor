from fastapi import FastAPI
from typing import Dict, Any

from engine.guard import should_execute
from engine.engine import execute_engine

app = FastAPI(title="Workflow Executor")


@app.post("/api/workflow/execute")
def execute_workflow(request: Dict[str, Any]):
    trace_id = request.get("trace_id")
    decision = request.get("decision")

    if not trace_id or not decision:
        return {
            "status": "failed",
            "error": "missing_trace_id_or_decision"
        }

    if not should_execute(decision):
        return {
            "trace_id": trace_id,
            "status": "skipped",
            "reason": "decision_not_workflow"
        }

    data = request.get("data")
    if not data or "payload" not in data:
        return {
            "trace_id": trace_id,
            "status": "failed",
            "error": "missing_workflow_payload"
        }

    result = execute_engine(data["payload"])

    return {
        "trace_id": trace_id,
        "status": "success" if result.get("success") else "failed",
        "execution_result": result
    }
