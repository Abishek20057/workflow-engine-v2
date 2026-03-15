def evaluate_rules(rules, data):

    rules = sorted(rules, key=lambda r: r["priority"])

    for rule in rules:

        condition = rule["condition"]

        if condition == "DEFAULT":
            return rule["next_step_id"]

        try:
            if eval(condition, {}, data):
                return rule["next_step_id"]
        except:
            pass

    return None