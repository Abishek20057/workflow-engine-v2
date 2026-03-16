from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

workflows = {}
steps = {}
rules = {}

workflow_counter = 1
step_counter = 1


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


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()


@app.get("/workflows")
def list_workflows():
    return [{"id": i, "name": w["name"]} for i, w in workflows.items()]


@app.post("/workflows")
def create_workflow(workflow: Workflow):
    global workflow_counter

    workflows[workflow_counter] = {
        "name": workflow.name,
        "steps": []
    }

    workflow_counter += 1

    return {"message": "Workflow created"}


@app.post("/workflows/{workflow_id}/steps")
def add_step(workflow_id: int, step: Step):

    global step_counter

    step_data = {
        "id": step_counter,
        "name": step.name,
        "type": step.step_type,
        "order": step.order,
        "rules": []
    }

    steps[step_counter] = step_data
    workflows[workflow_id]["steps"].append(step_counter)

    step_counter += 1

    return {"message": "Step added"}


@app.post("/steps/{step_id}/rules")
def add_rule(step_id: int, rule: Rule):

    rule_data = {
        "condition": rule.condition,
        "next_step_id": rule.next_step_id,
        "priority": rule.priority
    }

    steps[step_id]["rules"].append(rule_data)

    return {"message": "Rule added"}


@app.post("/workflows/{workflow_id}/execute")
def execute_workflow(workflow_id: int, execution: Execution):

    logs = []

    workflow_steps = workflows[workflow_id]["steps"]

    amount = execution.data.get("amount", 0)

    current_step = workflow_steps[0]

    while True:

        step = steps[current_step]

        logs.append(f"Executing Step: {step['name']}")

        next_step = None

        for rule in step["rules"]:

            condition = rule["condition"]

            if "amount" in condition:

                value = int(condition.split(">")[1])

                if amount > value:
                    next_step = rule["next_step_id"]

        if next_step is None:
            logs.append("Approved")
            break

        current_step = next_step

    return {"logs": logs}