from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import workflows,steps,rules,history
from engine import execute_engine

import uuid

app=FastAPI()

templates=Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/",response_class=HTMLResponse)
def home(request:Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "workflows":workflows.values(),
            "steps":steps.values()
        }
    )


@app.post("/workflow")
async def create_workflow(name:str):

    wid=str(uuid.uuid4())

    workflows[wid]={
        "id":wid,
        "name":name
    }

    return {"message":"workflow created"}


@app.post("/step")
async def create_step(workflow_id:str,name:str,step_type:str,order:int):

    sid=str(uuid.uuid4())

    steps[sid]={
        "id":sid,
        "workflow_id":workflow_id,
        "name":name,
        "type":step_type,
        "order":order
    }

    return {"message":"step created"}


@app.post("/rule")
async def create_rule(step_id:str,condition:str,next_step_id:str,priority:int):

    rid=str(uuid.uuid4())

    rules[rid]={
        "id":rid,
        "step_id":step_id,
        "condition":condition,
        "next":next_step_id,
        "priority":priority
    }

    return {"message":"rule created"}


@app.post("/execute/{workflow_id}",response_class=HTMLResponse)
async def run_workflow(request:Request,workflow_id:str):

    data=await request.json()

    amount=int(data["amount"])

    log,path=execute_engine(workflow_id,{"amount":amount})

    history.append({
        "workflow":workflow_id,
        "input":amount,
        "path":" → ".join(path)
    })

    return templates.TemplateResponse(
        "result.html",
        {
            "request":request,
            "logs":log
        }
    )


@app.get("/history",response_class=HTMLResponse)
def show_history(request:Request):

    return templates.TemplateResponse(
        "history.html",
        {
            "request":request,
            "history":history
        }
    )