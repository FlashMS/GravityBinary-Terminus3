from typing import Dict, Any, List

class HallucinationEvaluator:
    """
    Evaluator for the hallucination lane.
    Detects unsupported claims, invented facts, contradictions, and external knowledge violations.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.blocked_external = contract.get("blocked_external", [])
        self.required_grounding = contract.get("required_grounding", [])

    def evaluate(
        self,
        prompt: str,
        output: str,
        trace: List[str],
        oracle_trace: List[str],
    ) -> Dict[str, Any]:

        hallucinations = []

        # Check for external knowledge violations
        for phrase in self.blocked_external:
            if phrase.lower() in output.lower():
                hallucinations.append(f"EXTERNAL_KNOWLEDGE: {phrase}")

        # Check for unsupported claims (simple heuristic)
        for required in self.required_grounding:
            if required.lower() not in output.lower():
                hallucinations.append(f"MISSING_GROUNDING: {required}")

        # Check contradictions with oracle trace
        oracle_joined = " ".join(oracle_trace).lower()
        if output.lower() not in oracle_joined:
            hallucinations.append("ORACLE_CONTRADICTION")

        severity = self.classify_severity(hallucinations)
        explanation = self.build_explanation(hallucinations, severity)

        return {
            "lane": "hallucination",
            "hallucinations": hallucinations,
            "severity": severity,
            "explanation": explanation,
            "trace": trace,
            "oracle_trace": oracle_trace,
        }

    def classify_severity(self, hallucinations: List[str]) -> str:
        if not hallucinations:
            return "NONE"
        if any("EXTERNAL_KNOWLEDGE" in h for h in hallucinations):
            return "CRITICAL"
        if "ORACLE_CONTRADICTION" in hallucinations:
            return "SEVERE"
        if any("MISSING_GROUNDING" in h for h in hallucinations):
            return "MODERATE"
        return "MINOR"

    def build_explanation(self, hallucinations: List[str], severity: str) -> str:
        if not hallucinations:
            return "No hallucinations detected."

        parts = [f"Severity: {severity}"]

        for h in hallucinations:
            if "EXTERNAL_KNOWLEDGE" in h:
                parts.append("Model used external knowledge not allowed by instruction.")
            elif "ORACLE_CONTRADICTION" in h:
                parts.append("Model contradicted the oracle trace.")
            elif "MISSING_GROUNDING" in h:
                parts.append("Model failed to include required grounded information.")

        return " ".join(parts)
