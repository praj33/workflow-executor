Workflow Executor (Phase B)

This service turns assistant decisions into deterministic system executions.
It is execution-only. No UI. No intent logic.

Purpose

Execute workflows only when explicitly instructed

Ensure deterministic, traceable system actions

Act as the final execution layer in the assistant pipeline

Execution Gate

Execution happens only when:

"decision": "workflow"


All other decisions are safely skipped.

API Endpoint
POST /api/workflow/execute
Request Format
{
  "trace_id": "unique-id",
  "decision": "workflow",
  "data": {
    "workflow_type": "workflow",
    "payload": {
      "action_type": "task",
      "...": "workflow-specific fields"
    }
  }
}

Supported Workflows
action_type	Description
task	Task creation
reminder	Reminder scheduling
meeting	Meeting scheduling (mocked)
info	Read-only informational fetch

Unsupported actions fail explicitly.

Example Request (Task)
{
  "trace_id": "task-001",
  "decision": "workflow",
  "data": {
    "workflow_type": "workflow",
    "payload": {
      "action_type": "task",
      "title": "Submit payroll report"
    }
  }
}

Example Response
{
  "trace_id": "task-001",
  "status": "success",
  "execution_result": {
    "success": true,
    "task_id": "task_001",
    "title": "Submit payroll report"
  }
}

Run Locally
pip install -r requirements.txt
uvicorn main:app --reload


API docs available at:

http://127.0.0.1:8000/docs

Notes

No UI dependency

No async fan-out

One request → one execution path

All failures are explicit and traceable via trace_id