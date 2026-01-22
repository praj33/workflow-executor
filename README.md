# Workflow Executor  
**Production Deterministic Real-World Execution Engine**

Workflow Executor is the **single, authoritative execution layer** for the BHIV ecosystem.  
It converts approved assistant workflows into **deterministic, traceable real-world actions**.

This service is **execution-only**:
- No UI
- No reasoning
- No emotional logic

---

## 🎯 Purpose

- Execute workflows **only when explicitly approved**
- Enforce deterministic, single-path execution
- Guarantee explicit success / failure
- Preserve traceability across all products

---

## 🌐 Live Deployment

**Base URL**  
https://workflow-executor-mp4x.onrender.com  

**API Docs**  
https://workflow-executor-mp4x.onrender.com/docs  

**Primary Endpoint**
POST /api/workflow/execute

---

## 🔐 Execution Gate (Hard Rule)

Execution happens **only** when:
```json
"decision": "workflow"
```
All other decisions are safely skipped and logged.

## 📦 Request Contract
```json
{
  "trace_id": "unique-id",
  "decision": "workflow",
  "data": {
    "workflow_type": "workflow",
    "payload": {
      "action_type": "task"
    }
  }
}
```

## 🔌 Supported Execution Adapters
| action_type | Capability |
|-------------|------------|
| ai | External AI execution |
| whatsapp | Message delivery |
| email | Email dispatch |
| task | Task creation |
| reminder | Reminder scheduling |

Unsupported actions fail explicitly.

## ⚙️ Execution Guarantees

- One request → one execution path

- Adapter chosen only by action_type

- No retries, no hidden fallbacks

- No silent failures

- Stable response contract

- Full trace_id propagation

## 🧪 Verified Proof

- AI execution from AI Assistant

- Safe failure handling

- WhatsApp execution from Gurukul

- Task creation workflow

- Telemetry emitted to InsightFlow

- Cross-product trace chain verified

## 🚀 Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Docs**: http://127.0.0.1:8000/docs

## ✅ Final Status

- Shared execution service live

- All products routed through executor

- Determinism preserved

- Governance boundaries enforced

- Production ready

**Workflow Executor is now the live, stable, deterministic execution authority.**