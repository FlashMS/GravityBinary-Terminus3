from typing import Dict, Any, List


class OracleConsistencyEvaluator:
    """
    Evaluates oracle consistency across multiple runs.
    Checks whether oracle outputs and traces are stable.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.runs = contract.get("runs", 3)

    def evaluate(
        self,
        prompt: str,
        oracle_outputs: List[str],
        oracle_traces: List[List[str]],
    ) -> Dict[str, Any]:

        output_set = set(oracle_outputs)
        trace_set = set(tuple(t) for t in oracle_traces)

        output_drift = len(output_set) > 1
        trace_drift = len(trace_set) > 1

        issues = []
        if output_drift:
            issues.append("ORACLE_OUTPUT_VARIANCE")
        if trace_drift:
            issues.append("ORACLE_TRACE_VARIANCE")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity)

        return {
            "lane": "oracle_consistency",
            "prompt": prompt,
            "oracle_outputs": oracle_outputs,
            "oracle_traces": oracle_traces,
            "runs": self.runs,
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "ORACLE_OUTPUT_VARIANCE" in issues:
            return "CRITICAL"
        if "ORACLE_TRACE_VARIANCE" in issues:
            return "SEVERE"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str) -> str:
        if not issues:
            return "Oracle is consistent across all runs."

        parts = [f"Severity: {severity}"]
        for issue in issues:
            if issue == "ORACLE_OUTPUT_VARIANCE":
                parts.append("Oracle output changed across runs.")
            elif issue == "ORACLE_TRACE_VARIANCE":
                parts.append("Oracle trace changed across runs.")
        return " ".join(parts)
