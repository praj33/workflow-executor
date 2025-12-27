from fastapi import FastAPI, HTTPException
from typing import Any

from contracts.workflow_request import WorkflowExecuteRequest
from engine.guard import should_execute
from engine.engine import execute_engine
from utils.logger import get_logger

logger = get_logger()

app = FastAPI(title="Workflow Executor")


@app.post("/api/workflow/execute")
def execute_workflow(request: WorkflowExecuteRequest):
    trace_id = request.trace_id
    decision = request.decision

    logger.info(
        f"REQUEST_RECEIVED | trace_id={trace_id} | decision={decision}"
    )

    # Guard: execute ONLY when decision == "workflow"
    if not should_execute(decision):
        logger.info(
            f"EXECUTION_SKIPPED | trace_id={trace_id} | reason=decision_not_workflow"
        )
        return {
            "trace_id": trace_id,
            "status": "skipped",
            "reason": "decision_not_workflow"
        }

    if not request.data or not request.data.payload:
        logger.error(
            f"EXECUTION_FAILED | trace_id={trace_id} | error_code=missing_workflow_payload"
        )
        raise HTTPException(
            status_code=400,
            detail="missing_workflow_payload"
        )

    payload = request.data.payload
    action_type = payload.get("action_type")

    logger.info(
        f"EXECUTION_STARTED | trace_id={trace_id} | action_type={action_type}"
    )

    result = execute_engine(payload)

    if result.get("success"):
        logger.info(
            f"EXECUTION_SUCCESS | trace_id={trace_id} | action_type={action_type}"
        )
    else:
        logger.error(
            f"EXECUTION_FAILED | trace_id={trace_id} | action_type={action_type} "
            f"| error_code={result.get('error_code')}"
        )

    return {
        "trace_id": trace_id,
        "status": "success" if result.get("success") else "failed",
        "execution_result": result
    }
