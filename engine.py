from models import steps, rules

def run_engine(workflow_id, amount):

    logs = []
    path = []

    logs.append("🚀 Workflow Started")

    workflow_steps = [s for s in steps.values() if s["workflow_id"] == workflow_id]
    workflow_steps = sorted(workflow_steps, key=lambda x: x["order"])

    for step in workflow_steps:

        logs.append(f"Step : {step['name']}")
        path.append(step["name"])

        step_rules = [r for r in rules.values() if r["step_id"] == step["id"]]

        for rule in step_rules:

            if "amount" in rule["condition"]:
                limit = int(rule["condition"].split(">")[1])

                if amount > limit:
                    logs.append("Condition TRUE → Moving Next")
                else:
                    logs.append("Condition FALSE")

    logs.append("✅ Workflow Completed")

    return logs, path