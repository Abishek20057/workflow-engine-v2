from models import steps, rules

def execute_engine(workflow_id, data):

    log=[]
    path=[]

    log.append("🚀 Workflow Started")

    current_steps=[s for s in steps.values() if s["workflow_id"]==workflow_id]
    current_steps=sorted(current_steps,key=lambda x:x["order"])

    for step in current_steps:

        log.append(f"📋 Step : {step['name']}")
        path.append(step['name'])

        step_rules=[r for r in rules.values() if r["step_id"]==step["id"]]

        for r in step_rules:

            condition=r["condition"]

            if "amount" in condition:

                limit=int(condition.split(">")[1])

                if data["amount"]>limit:

                    log.append("✅ Condition TRUE")

                else:

                    log.append("❌ Condition FALSE")

    log.append("🎉 Workflow Completed")

    return log,path