from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import Workflow, Step, Rule, Execution
from workflow_engine import evaluate_rules

app = FastAPI()

# In-memory storage
workflows = []
steps = []
rules = []
executions = []


# Home page
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()


# Create workflow
@app.post("/workflows")
def create_workflow(workflow: Workflow):

    wf = workflow.dict()
    wf["id"] = str(len(workflows) + 1)

    workflows.append(wf)

    return wf


# List workflows
@app.get("/workflows")
def list_workflows():
    return workflows


# Add step
@app.post("/workflows/{workflow_id}/steps")
def add_step(workflow_id: str, step: Step):

    s = step.dict()
    s["id"] = str(len(steps) + 1)

    steps.append(s)

    return s


# Add rule
@app.post("/steps/{step_id}/rules")
def add_rule(step_id: str, rule: Rule):

    r = rule.dict()
    r["id"] = str(len(rules) + 1)

    rules.append(r)

    return r


# Execute workflow
@app.post("/workflows/{workflow_id}/execute")
def execute_workflow(workflow_id: str, execution: Execution):

    data = execution.data

    workflow_steps = [s for s in steps if s["workflow_id"] == workflow_id]

    if not workflow_steps:
        return {"error": "No steps found for this workflow"}

    current_step = sorted(workflow_steps, key=lambda x: x["order"])[0]

    logs = []

    while current_step:

        logs.append(f"Executing step: {current_step['name']}")

        step_rules = [r for r in rules if r["step_id"] == current_step["id"]]

        next_step_id = evaluate_rules(step_rules, data)

        if next_step_id is None:
            logs.append("Workflow finished")
            break

        next_steps = [s for s in steps if s["id"] == next_step_id]

        if not next_steps:
            logs.append("Next step not found")
            break

        current_step = next_steps[0]

    execution_log = {
        "workflow_id": workflow_id,
        "logs": logs
    }

    executions.append(execution_log)

    return execution_log