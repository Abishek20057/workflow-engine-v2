from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

workflows = {}
steps = {}

workflow_id = 1
step_id = 1


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/approval.html", response_class=HTMLResponse)
def approval():
    with open("templates/approval.html", encoding="utf-8") as f:
        return f.read()


@app.get("/workflows")
def get_workflows():
    return list(workflows.values())


@app.post("/workflows")
def create_workflow(data: dict):
    global workflow_id

    workflows[workflow_id] = {
        "id": workflow_id,
        "name": data["name"]
    }

    workflow_id += 1

    return {"message": "workflow created"}


@app.post("/workflows/{wf_id}/steps")
def add_step(wf_id: int, data: dict):
    global step_id

    steps[step_id] = {
        "id": step_id,
        "workflow": wf_id,
        "name": data["name"]
    }

    step_id += 1

    return {"message": "step added"}


@app.post("/execute")
def execute(data: dict):

    amount = data["amount"]

    if amount > 1000:
        status = "approved"
    else:
        status = "manager"

    return {"status": status}