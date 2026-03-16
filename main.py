from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import engine
from models import Workflow, Step, Rule, ExecutionInput

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "workflows": engine.workflows,
            "steps": engine.steps,
            "history": engine.execution_history
        }
    )


@app.post("/workflow")
def create_workflow(w: Workflow):

    wid = engine.create_workflow(w.name)

    return {"workflow_id": wid}


@app.post("/step")
def create_step(s: Step):

    sid = engine.create_step(
        s.workflow_id,
        s.name,
        s.step_type,
        s.order
    )

    return {"step_id": sid}


@app.post("/rule")
def create_rule(r: Rule):

    rid = engine.create_rule(
        r.step_id,
        r.condition,
        r.next_step_id,
        r.priority
    )

    return {"rule_id": rid}


@app.post("/execute/{workflow_id}")
def execute(workflow_id: str, data: ExecutionInput):

    logs = engine.execute_workflow(workflow_id, data.data)

    return {"logs": logs}