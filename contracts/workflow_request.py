from typing import TypedDict, Literal, Optional, Dict, Any

DecisionType = Literal[
    "respond",
    "task",
    "workflow",
    "insight",
    "fallback"
]

class WorkflowData(TypedDict):
    workflow_type: Literal["workflow"]
    payload: Dict[str, Any]

class WorkflowExecuteRequest(TypedDict):
    trace_id: str
    decision: DecisionType
    data: Optional[WorkflowData]
