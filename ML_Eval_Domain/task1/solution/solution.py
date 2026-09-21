import sys, json

def evaluate_case(case):
    oracle_trace = case["oracle_trace"]
    model_trace = case["model_trace"]
    issues = []

    if len(model_trace) < len(oracle_trace):
        issues.append("STEP_SKIPPING")
    if len(model_trace) > len(oracle_trace) + 2:
        issues.append("STEP_INVENTION")
    if any("unrelated" in step.lower() for step in model_trace):
        issues.append("SCOPE_DRIFT")

    drift = bool(issues)
    score = 1.0 if not issues else max(0.0, 1.0 - 0.2 * len(issues))

    return {
        "drift": drift,
        "reasons": issues,
        "score": score,
    }

data = json.load(sys.stdin)
results = [evaluate_case(case) for case in data["cases"]]
json.dump({"results": results}, sys.stdout)
