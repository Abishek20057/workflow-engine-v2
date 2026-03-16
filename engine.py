workflows = {}
steps = {}
rules = {}

execution_history = []

workflow_counter = 1
step_counter = 1
rule_counter = 1


def create_workflow(name):

    global workflow_counter

    wid = f"wf_{workflow_counter}"

    workflows[wid] = {
        "id": wid,
        "name": name
    }

    workflow_counter += 1

    return wid


def create_step(workflow_id, name, step_type, order):

    global step_counter

    sid = f"step_{step_counter}"

    steps[sid] = {
        "id": sid,
        "workflow_id": workflow_id,
        "name": name,
        "type": step_type,
        "order": order
    }

    step_counter += 1

    return sid


def create_rule(step_id, condition, next_step_id, priority):

    global rule_counter

    rid = f"rule_{rule_counter}"

    rules[rid] = {
        "step_id": step_id,
        "condition": condition,
        "next_step_id": next_step_id,
        "priority": priority
    }

    rule_counter += 1

    return rid


def execute_workflow(workflow_id, data):

    logs = []

    logs.append("Start Workflow")

    wf_steps = [s for s in steps.values() if s["workflow_id"] == workflow_id]

    wf_steps = sorted(wf_steps, key=lambda x: x["order"])

    if not wf_steps:

        logs.append("No steps found")

        return logs

    current_step = wf_steps[0]

    path = []

    while current_step:

        logs.append("Step : " + current_step["name"])

        path.append(current_step["name"])

        step_rules = [r for r in rules.values() if r["step_id"] == current_step["id"]]

        next_step = None

        for rule in step_rules:

            try:

                if eval(rule["condition"], {}, data):

                    logs.append("Condition TRUE")

                    next_step = steps.get(rule["next_step_id"])

                    break

                else:

                    logs.append("Condition FALSE")

            except:

                logs.append("Condition Error")

        if next_step:

            current_step = next_step

        else:

            break

    logs.append("Workflow Completed")

    execution_history.append({

        "workflow": workflow_id,

        "input": data,

        "path": " → ".join(path)

    })

    return logs