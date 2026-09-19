from typing import Dict, Any, List

class ConstraintAdherenceEvaluator:
    """
    Evaluator for the constraint_adherence lane.
    Checks whether the model violated explicit constraints in the instruction.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.forbidden_phrases = contract.get("forbidden_phrases", [])
        self.required_format = contract.get("required_format", None)

    def evaluate(
        self,
        prompt: str,
        output: str,
        trace: List[str],
        oracle_trace: List[str],
    ) -> Dict[str, Any]:

        violations = []

        # Forbidden phrase check
        for phrase in self.forbidden_phrases:
            if phrase.lower() in output.lower():
                violations.append(f"FORBIDDEN_PHRASE: {phrase}")

        # Required format check
        if self.required_format:
            if not output.strip().startswith(self.required_format):
                violations.append("FORMAT_VIOLATION")

        severity = self.classify_severity(violations)
        explanation = self.build_explanation(violations, severity)

        return {
            "lane": "constraint_adherence",
            "violations": violations,
            "severity": severity,
            "explanation": explanation,
            "trace": trace,
            "oracle_trace": oracle_trace,
        }

    def classify_severity(self, violations: List[str]) -> str:
        if not violations:
            return "NONE"
        if any("FORBIDDEN_PHRASE" in v for v in violations):
            return "CRITICAL"
        if "FORMAT_VIOLATION" in violations:
            return "MODERATE"
        return "MINOR"

    def build_explanation(self, violations: List[str], severity: str) -> str:
        if not violations:
            return "No constraint violations detected."

        parts = [f"Severity: {severity}"]

        for v in violations:
            if "FORBIDDEN_PHRASE" in v:
                parts.append("Model used a forbidden phrase.")
            elif "FORMAT_VIOLATION" in v:
                parts.append("Model did not follow required output format.")

        return " ".join(parts)
