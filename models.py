from pydantic import BaseModel


class Workflow(BaseModel):
    name: str


class Step(BaseModel):
    workflow_id: str
    name: str
    step_type: str
    order: int


class Rule(BaseModel):
    step_id: str
    condition: str
    next_step_id: str
    priority: int


class ExecutionInput(BaseModel):
    data: dict