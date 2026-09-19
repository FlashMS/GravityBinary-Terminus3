from typing import Dict, Any, List

class DeterminismEvaluator:
    """
    Evaluator for determinism detection.
    Checks whether multiple simulated model outputs differ.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.runs = contract.get("runs", 3)

    def evaluate(
        self,
        prompt: str,
        outputs: List[str],
        traces: List[List[str]],
        oracle_trace: List[str],
    ) -> Dict[str, Any]:

        # Check output variance
        output_set = set(outputs)
        trace_set = set(tuple(t) for t in traces)

        output_drift = len(output_set) > 1
        trace_drift = len(trace_set) > 1

        issues = []
        if output_drift:
            issues.append("OUTPUT_VARIANCE")
        if trace_drift:
            issues.append("TRACE_VARIANCE")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity)

        return {
            "lane": "determinism",
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
            "outputs": outputs,
            "traces": traces,
            "oracle_trace": oracle_trace,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "OUTPUT_VARIANCE" in issues:
            return "CRITICAL"
        if "TRACE_VARIANCE" in issues:
            return "SEVERE"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str) -> str:
        if not issues:
            return "Deterministic across all runs."

        parts = [f"Severity: {severity}"]

        for issue in issues:
            if issue == "OUTPUT_VARIANCE":
                parts.append("Model output changed across runs.")
            elif issue == "TRACE_VARIANCE":
                parts.append("Model trace changed across runs.")

        return " ".join(parts)
