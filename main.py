from fastapi import FastAPI, HTTPException
import traceback

from contracts.workflow_request import WorkflowExecuteRequest
from execution_engine.guard import should_execute
from execution_engine.engine import execute_engine
from utils.logger import get_logger
from config.settings import settings

logger = get_logger()

app = FastAPI(
    title="Workflow Executor",
    description="Deterministic execution layer for assistant workflows",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event():
    logger.info(
        f"SERVICE_STARTUP | service={settings.service_name} | env={settings.environment}"
    )


@app.post("/api/workflow/execute")
def execute_workflow(request: WorkflowExecuteRequest):
    trace_id = request.trace_id
    decision = request.decision

    logger.info(
        f"REQUEST_RECEIVED | trace_id={trace_id} | decision={decision}"
    )

    try:
        # Guard: execute ONLY when decision == "workflow"
        if not should_execute(decision):
            logger.info(
                f"EXECUTION_SKIPPED | trace_id={trace_id} | reason=decision_not_workflow"
            )
            return {
                "trace_id": trace_id,
                "status": "skipped",
                "reason": "decision_not_workflow",
            }

        if not request.data or not request.data.payload:
            logger.error(
                f"EXECUTION_FAILED | trace_id={trace_id} | error_code=missing_workflow_payload"
            )
            raise HTTPException(
                status_code=400,
                detail="missing_workflow_payload",
            )

        payload = request.data.payload
        action_type = payload.get("action_type")

        logger.info(
            f"EXECUTION_STARTED | trace_id={trace_id} | action_type={action_type}"
        )

        result = execute_engine(payload)

        if result.get("success") is True:
            logger.info(
                f"EXECUTION_SUCCESS | trace_id={trace_id} | action_type={action_type}"
            )
            status = "success"
        else:
            logger.error(
                f"EXECUTION_FAILED | trace_id={trace_id} | action_type={action_type} "
                f"| error_code={result.get('error_code')}"
            )
            status = "failed"

        return {
            "trace_id": trace_id,
            "status": status,
            "execution_result": result,
        }

    except HTTPException:
        # Explicit failure
        raise

    except Exception as e:
        # Hard safety boundary (never crash outward)
        logger.error(
            f"EXECUTION_CRASH | trace_id={trace_id} | exception={str(e)}"
        )
        logger.debug(traceback.format_exc())

        return {
            "trace_id": trace_id,
            "status": "failed",
            "execution_result": {
                "success": False,
                "error_code": "internal_execution_error",
                "message": "Execution failed due to internal error",
            },
        }
