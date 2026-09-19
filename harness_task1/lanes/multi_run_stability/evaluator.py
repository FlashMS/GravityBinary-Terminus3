from typing import Dict, Any, List


class MultiRunStabilityEvaluator:
    """
    Evaluates stability across multiple runs.
    Checks whether solver outputs and traces are stable.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.runs = contract.get("runs", 5)

    def evaluate(
        self,
        prompt: str,
        solver_outputs: List[str],
        solver_traces: List[List[str]],
    ) -> Dict[str, Any]:

        output_set = set(solver_outputs)
        trace_set = set(tuple(t) for t in solver_traces)

        output_drift = len(output_set) > 1
        trace_drift = len(trace_set) > 1

        issues = []
        if output_drift:
            issues.append("SOLVER_OUTPUT_VARIANCE")
        if trace_drift:
            issues.append("SOLVER_TRACE_VARIANCE")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity)

        return {
            "lane": "multi_run_stability",
            "prompt": prompt,
            "solver_outputs": solver_outputs,
            "solver_traces": solver_traces,
            "runs": self.runs,
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "SOLVER_OUTPUT_VARIANCE" in issues:
            return "CRITICAL"
        if "SOLVER_TRACE_VARIANCE" in issues:
            return "SEVERE"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str) -> str:
        if not issues:
            return "Solver is stable across runs."

        parts = [f"Severity: {severity}"]
        for issue in issues:
            if issue == "SOLVER_OUTPUT_VARIANCE":
                parts.append("Solver outputs vary across runs.")
            elif issue == "SOLVER_TRACE_VARIANCE":
                parts.append("Solver traces vary across runs.")
        return " ".join(parts)
