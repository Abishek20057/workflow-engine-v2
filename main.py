from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ===== DATA =====
workflows = {}
steps = {}
rules = {}
history = []

# ===== HOME =====
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ===== CREATE WORKFLOW =====
@app.post("/workflow")
def create_workflow(name: str):
    wf_id = f"wf_{len(workflows)+1}"
    workflows[wf_id] = {"id": wf_id, "name": name}

    # default steps (IMPORTANT for demo)
    steps[wf_id] = [
        {"name": "Manager Approval", "order": 1},
        {"name": "Finance Approval", "order": 2},
        {"name": "Final Approval", "order": 3}
    ]

    rules[wf_id] = [
        {"condition": "amount > 1000", "next_step": 2}
    ]

    return {"msg": "created"}

# ===== GET WORKFLOWS =====
@app.get("/get_workflows")
def get_workflows():
    return list(workflows.values())

# ===== GET STEPS =====
@app.get("/get_steps/{wf_id}")
def get_steps(wf_id: str):
    return steps.get(wf_id, [])

# ===== EXECUTE =====
@app.get("/execute/{wf_id}", response_class=HTMLResponse)
def execute(wf_id: str, amount: int = 0, country: str = "", request: Request = None):

    wf_steps = steps.get(wf_id, [])
    wf_rules = rules.get(wf_id, [])

    path = []
    current_order = 1

    while True:
        step = next((s for s in wf_steps if s["order"] == current_order), None)
        if not step:
            break

        path.append(step["name"])
        moved = False

        for rule in wf_rules:
            try:
                if eval(rule["condition"]):
                    current_order = rule["next_step"]
                    moved = True
                    break
            except:
                pass

        if not moved:
            current_order += 1

    history.append({
        "wf": wf_id,
        "amount": amount,
        "country": country,
        "path": " → ".join(path)
    })

    return templates.TemplateResponse("result.html", {
        "request": request,
        "path": path
    })

# ===== HISTORY =====
@app.get("/history", response_class=HTMLResponse)
def view_history(request: Request):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history
    })