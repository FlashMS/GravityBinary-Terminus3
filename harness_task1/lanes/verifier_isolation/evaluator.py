from typing import Dict, Any, List


class VerifierIsolationEvaluator:
    """
    Evaluates verifier isolation.
    Checks that verifier decisions are stable and do not depend
    on solver outputs or external noise.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.runs = contract.get("runs", 3)

    def evaluate(
        self,
        prompt: str,
        solver_outputs: List[str],
        verifier_decisions: List[str],
    ) -> Dict[str, Any]:

        decision_set = set(verifier_decisions)
        depends_on_solver = self._depends_on_solver(solver_outputs, verifier_decisions)

        issues = []
        if len(decision_set) > 1:
            issues.append("VERIFIER_DECISION_VARIANCE")
        if depends_on_solver:
            issues.append("VERIFIER_DEPENDS_ON_SOLVER_OUTPUT")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity)

        return {
            "lane": "verifier_isolation",
            "prompt": prompt,
            "solver_outputs": solver_outputs,
            "verifier_decisions": verifier_decisions,
            "runs": self.runs,
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
        }

    def _depends_on_solver(
        self,
        solver_outputs: List[str],
        verifier_decisions: List[str],
    ) -> bool:
        # Simple heuristic: if decisions change when solver outputs change,
        # we treat that as dependence.
        pairs = list(zip(solver_outputs, verifier_decisions))
        unique_pairs = set(pairs)
        return len(unique_pairs) > 1

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "VERIFIER_DEPENDS_ON_SOLVER_OUTPUT" in issues:
            return "CRITICAL"
        if "VERIFIER_DECISION_VARIANCE" in issues:
            return "SEVERE"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str) -> str:
        if not issues:
            return "Verifier is isolated and stable across runs."

        parts = [f"Severity: {severity}"]
        for issue in issues:
            if issue == "VERIFIER_DECISION_VARIANCE":
                parts.append("Verifier decisions vary across runs.")
            elif issue == "VERIFIER_DEPENDS_ON_SOLVER_OUTPUT":
                parts.append("Verifier decisions depend on solver outputs.")
        return " ".join(parts)
