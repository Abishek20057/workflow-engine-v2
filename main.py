from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

workflows = []
steps = []
rules = []


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/approval.html")
def approval():
    return FileResponse("approval.html")


@app.get("/workflows")
def get_workflows():
    return workflows


@app.post("/workflows")
def create_workflow(data: dict):

    wf = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "version": 1
    }

    workflows.append(wf)

    return wf


@app.post("/workflows/{workflow_id}/steps")
def add_step(workflow_id: str, data: dict):

    step = {
        "id": str(uuid.uuid4()),
        "workflow_id": workflow_id,
        "name": data["name"],
        "step_type": data["step_type"],
        "order": data["order"]
    }

    steps.append(step)

    return step


@app.post("/steps/{step_id}/rules")
def add_rule(step_id: str, data: dict):

    rule = {
        "id": str(uuid.uuid4()),
        "step_id": step_id,
        "condition": data["condition"],
        "next_step_id": data["next_step_id"],
        "priority": data["priority"]
    }

    rules.append(rule)

    return rule


@app.post("/workflows/{workflow_id}/execute")
def execute(workflow_id: str, data: dict):

    amount = data["data"]["amount"]

    logs = []

    if amount > 1000:

        logs.append("Manager Approval Required")

        if amount > 10000:
            logs.append("Finance Approval Required")
            logs.append("Expense Approved")

        else:
            logs.append("Expense Approved")

    else:
        logs.append("Expense Approved")

    return {"logs": logs}