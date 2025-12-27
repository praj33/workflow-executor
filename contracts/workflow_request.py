from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class WorkflowData(BaseModel):
    workflow_type: Literal["workflow"] = Field(
        ..., description="Meta indicator for downstream execution"
    )
    payload: Dict[str, Any] = Field(
        ..., description="Structured execution payload"
    )


class WorkflowExecuteRequest(BaseModel):
    trace_id: str = Field(..., min_length=1)
    decision: Literal["respond", "task", "workflow", "insight", "fallback"]
    data: Optional[WorkflowData] = None
