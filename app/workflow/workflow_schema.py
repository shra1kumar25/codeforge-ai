from pydantic import BaseModel
from typing import Any


class WorkflowStep(BaseModel):
    id: str
    name: str
    type: str
    config: dict[str, Any] = {}


class Workflow(BaseModel):
    id: str
    name: str
    steps: list[WorkflowStep]
