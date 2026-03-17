from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ================= DATA =================
workflows = {}
steps = {}
rules = {}
history = []

# ================= HOME =================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ================= CREATE WORKFLOW =================
@app.post("/workflow")
def create_workflow(name: str):
    wf_id = f"wf_{len(workflows)+1}"
    workflows[wf_id] = {"id": wf_id, "name": name}
    steps[wf_id] = []
    rules[wf_id] = []
    return {"message": "created"}

# ================= GET WORKFLOWS =================
@app.get("/get_workflows")
def get_workflows():
    return list(workflows.values())

# ================= ADD STEP =================
@app.post("/step")
def add_step(wf_id: str, name: str, order: int):
    steps[wf_id].append({
        "name": name,
        "order": order
    })
    steps[wf_id] = sorted(steps[wf_id], key=lambda x: x["order"])
    return {"message": "step added"}

# ================= ADD RULE =================
@app.post("/rule")
def add_rule(wf_id: str, condition: str, next_step: int):
    rules[wf_id].append({
        "condition": condition,
        "next_step": next_step
    })
    return {"message": "rule added"}

# ================= EXECUTE =================
@app.get("/execute/{wf_id}", response_class=HTMLResponse)
def execute(wf_id: str, amount: int = 0, country: str = "", request: Request = None):

    wf_steps = steps.get(wf_id, [])
    wf_rules = rules.get(wf_id, [])

    path = []
    current_index = 0

    while current_index < len(wf_steps):
        step = wf_steps[current_index]
        path.append(step["name"])

        moved = False

        for rule in wf_rules:
            try:
                if eval(rule["condition"]):
                    current_index = rule["next_step"]
                    moved = True
                    break
            except:
                pass

        if not moved:
            current_index += 1

    # Save history
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

# ================= HISTORY =================
@app.get("/history", response_class=HTMLResponse)
def view_history(request: Request):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history
    })