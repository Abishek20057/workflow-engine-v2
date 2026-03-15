from pydantic import BaseModel
from typing import Optional


class Workflow(BaseModel):
    name: str
    version: int
    is_active: bool


class Step(BaseModel):
    workflow_id: str
    name: str
    step_type: str
    order: int


class Rule(BaseModel):
    step_id: str
    condition: str
    next_step_id: Optional[str]
    priority: int


class Execution(BaseModel):
    workflow_id: str
    data: dict