from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import workflows, steps, rules, history
from engine import run_engine

app = FastAPI()

# ===================== STATIC + TEMPLATE =====================
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ===================== HOME =====================
@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ===================== CREATE WORKFLOW =====================
@app.post("/workflow")
def create_workflow(name: str):
    workflow_id = f"wf_{len(workflows) + 1}"

    workflows[workflow_id] = {
        "id": workflow_id,
        "name": name
    }

    return {"id": workflow_id}


# ===================== GET WORKFLOWS =====================
@app.get("/get_workflows")
def get_workflows():
    return list(workflows.values())


# ===================== ADD STEP =====================
@app.post("/step")
def add_step(workflow_id: str, name: str, step_type: str, order: int):

    step_id = f"step_{len(steps) + 1}"

    steps[step_id] = {
        "id": step_id,
        "workflow_id": workflow_id,
        "name": name,
        "type": step_type,
        "order": order
    }

    return {"id": step_id}


# ===================== GET STEPS =====================
@app.get("/get_steps/{workflow_id}")
def get_steps(workflow_id: str):
    return [
        s for s in steps.values()
        if s["workflow_id"] == workflow_id
    ]


# ===================== ADD RULE =====================
@app.post("/rule")
def add_rule(step_id: str, condition: str, next_step_id: str, priority: int):

    rule_id = f"rule_{len(rules) + 1}"

    rules[rule_id] = {
        "id": rule_id,
        "step_id": step_id,
        "condition": condition,
        "next_step_id": next_step_id,
        "priority": priority
    }

    return {"id": rule_id}


# ===================== GET RULES =====================
@app.get("/get_rules/{step_id}")
def get_rules(step_id: str):
    return [
        r for r in rules.values()
        if r["step_id"] == step_id
    ]


# ===================== EXECUTE WORKFLOW =====================
@app.api_route("/execute/{workflow_id}", methods=["GET", "POST"], response_class=HTMLResponse)
def execute(request: Request, workflow_id: str, amount: int = 0, country: str = "IN"):

    logs, path = run_engine(workflow_id, amount)

    # SAVE HISTORY
    history.append({
        "workflow": workflow_id,
        "amount": amount,
        "country": country,
        "path": " → ".join(path)
    })

    return templates.TemplateResponse("result.html", {
        "request": request,
        "logs": logs,
        "country": country
    })


# ===================== HISTORY =====================
@app.get("/history", response_class=HTMLResponse)
def view_history(request: Request):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history
    })