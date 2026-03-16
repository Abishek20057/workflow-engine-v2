from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# serve css files
app.mount("/static", StaticFiles(directory="static"), name="static")

# in-memory database
workflows = {}
steps = {}
rules = {}

workflow_id = 1
step_id = 1


class Workflow(BaseModel):
    name: str


class Step(BaseModel):
    name: str
    step_type: str
    order: int


class Rule(BaseModel):
    condition: str
    next_step_id: int
    priority: int


class Execution(BaseModel):
    data: dict


# ---------------- HOME PAGE ----------------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


# ---------------- WORKFLOWS ----------------

@app.get("/workflows")
def list_workflows():
    return [{"id": i, "name": w["name"]} for i, w in workflows.items()]


@app.post("/workflows")
def create_workflow(workflow: Workflow):
    global workflow_id

    workflows[workflow_id] = {
        "name": workflow.name,
        "steps": []
    }

    workflow_id += 1

    return {"message": "Workflow created"}


# ---------------- STEPS ----------------

@app.post("/workflows/{wf_id}/steps")
def add_step(wf_id: int, step: Step):

    global step_id

    step_data = {
        "id": step_id,
        "name": step.name,
        "type": step.step_type,
        "order": step.order,
        "rules": []
    }

    steps[step_id] = step_data

    workflows[wf_id]["steps"].append(step_id)

    step_id += 1

    return {"message": "Step added"}


# ---------------- RULES ----------------

@app.post("/steps/{step_id}/rules")
def add_rule(step_id: int, rule: Rule):

    rule_data = {
        "condition": rule.condition,
        "next_step_id": rule.next_step_id,
        "priority": rule.priority
    }

    steps[step_id]["rules"].append(rule_data)

    return {"message": "Rule added"}


# ---------------- EXECUTION ----------------

@app.post("/workflows/{wf_id}/execute")
def execute_workflow(wf_id: int, execution: Execution):

    logs = []

    wf_steps = workflows[wf_id]["steps"]

    amount = execution.data.get("amount", 0)

    current = wf_steps[0]

    while True:

        step = steps[current]

        logs.append(f"Executing step: {step['name']}")

        next_step = None

        for rule in step["rules"]:

            cond = rule["condition"]

            if "amount" in cond:

                value = int(cond.split(">")[1])

                if amount > value:
                    next_step = rule["next_step_id"]

        if next_step is None:
            logs.append("Approved")
            break

        current = next_step

    return {"logs": logs}