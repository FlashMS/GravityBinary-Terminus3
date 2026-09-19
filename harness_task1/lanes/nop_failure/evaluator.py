from typing import Dict, Any, List


class NopFailureEvaluator:
    """
    Evaluates whether the verifier correctly rejects NOP / trivial outputs.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def evaluate(self, agent_output: str) -> Dict[str, Any]:
        issues: List[str] = []

        normalized = agent_output.strip().lower()

        nop_patterns = [
            "",
            "nop",
            "no-op",
            "no op",
            "i cannot solve this",
            "i can't solve this",
            "done",
            "ok",
            "success",
            "pass",
            "skip",
            "no output",
            "null",
            "undefined",
        ]

        if normalized in nop_patterns:
            issues.append("NOP_OUTPUT")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity, agent_output)

        return {
            "lane": "nop_failure",
            "severity": severity,
            "prompt": self.contract.get("description", "NOP failure check"),
            "explanation": explanation,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "NOP_OUTPUT" in issues:
            return "CRITICAL"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str, agent_output: str) -> str:
        if not issues:
            return "Verifier correctly rejects NOP outputs or no NOP was detected."
        return (
            f"Severity: {severity}. Issues: {', '.join(issues)}. "
            f"Agent output: {repr(agent_output)}."
        )
