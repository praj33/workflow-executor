# Workflow Executor  
**Phase D + Phase E — Production Integrated Real-World Execution Engine**

The Workflow Executor converts assistant decisions into **deterministic, real-world system executions**.

This service is **execution-only**:
- No UI
- No intent reasoning
- No emotional logic

It is the **final execution authority** in the assistant pipeline.

---

## 🎯 Purpose

- Execute workflows **only** when explicitly instructed
- Guarantee deterministic, traceable system actions
- Enforce strict success / failure boundaries
- Act as the last controlled layer before real-world effects

---

## 🌐 Live Deployment

**Base URL**  
https://workflow-executor-rzfq.onrender.com  

**Swagger / OpenAPI Docs**  
https://workflow-executor-rzfq.onrender.com/docs  

**Primary Endpoint**  
 
POST /api/workflow/execute

## 🔐 Execution Gate (Non-Negotiable)

Execution occurs **only** when:

```json
"decision": "workflow"

```

All other decisions are safely skipped.

## API Endpoint
`POST /api/workflow/execute`

### Request Format
```json
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

```

## Supported Workflows
| action_type | Description                  |
|-------------|------------------------------|
| task        | Task creation                |
| reminder    | Reminder scheduling          |
| meeting     | Meeting scheduling (mocked)  |
| info        | Read-only informational fetch|

Unsupported actions fail explicitly.

## 🚀 Phase E — Real-World Execution Adapters

Phase E extends the executor from logical workflows to real ecosystem actions, while preserving all determinism guarantees.

## 🚀 Supported Execution Adapters (Phase E)

| Adapter      | Status | Description                                             |
|-------------|--------|---------------------------------------------------------|
| WhatsApp    | ✅     | Deterministic message execution (provider or mock)      |
| Email       | ✅     | Email sending via SMTP / API (or hardened mock)         |
| AI API      | ✅     | External AI call with structured, deterministic output |
| Task System | ✅     | Persistent task registry / external task tool          |

## Adapters are:

- Isolated

- Deterministic

- Failure-explicit

- Pluggable without contract drift

## 🔧 Adapter Routing (Phase E)

- Adapter selected only by action_type

- Exactly one adapter executes per request

- Unsupported adapters → explicit failure

- Adapter crashes → explicit failure

- No retries, no hidden fallbacks

## Example Request (Task)
```json
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
```

## Example Response
```json
{
  "trace_id": "task-001",
  "status": "success",
  "execution_result": {
    "success": true,
    "task_id": "task_001",
    "title": "Submit payroll report"
  }
}
```

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs available at: http://127.0.0.1:8000/docs

## Notes
- No UI dependency  
- No async fan-out  
- One request → one execution path  
- All failures are explicit and traceable via `trace_id`

## Phase C Status

- Strict schema validation enforced
- Deterministic execution (single-path)
- Explicit failure states
- Full traceability via logs
- Unit tests passing
- Integration verified with real payloads

## Phase D Status — Real World Integration

- Assistant → Decision Hub → Executor wired
- Production-grade logging
- Hosted endpoint live
- Real payload integration verified
- Demo-safe execution guarantees

## ✅ Phase E Status — Completed

- Real-world execution adapters implemented
- Deterministic adapter routing
- External system calls hardened
- Explicit adapter failure handling
- Trace-chain proof verified
- No contract drift introduced

### Capabilities
- Live ecosystem execution (assistant → decision hub → executor)
- Real-world–ready execution adapters (pluggable system hooks)
- Deterministic single-path execution
- Explicit failure states with hard boundaries
- Graceful degradation with last-resort safety net
- Full traceability via `trace_id` across all layers

### Operational Guarantees
- No execution unless `decision === "workflow"`
- No silent failures
- No ambiguous outcomes
- No contract drift
- Stable, frontend-safe response format

### Readiness
- Environment-driven configuration
- Hosted endpoint ready
- Logs are production-grade and auditable
- End-to-end integration verified
- Performance sanity checked

### Final Declaration
**Execution Layer is now live, stable, integrated, deterministic and production usable.**

