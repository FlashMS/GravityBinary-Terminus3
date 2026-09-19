from typing import Dict, Any, List


class StepCorrectnessEvaluator:
    """
    Evaluator for step correctness.
    Compares model reasoning steps against oracle steps.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def evaluate(
        self,
        prompt: str,
        output: str,
        trace: List[str],
        oracle_trace: List[str],
    ) -> Dict[str, Any]:

        issues = []
        step_alignment = self.compare_steps(trace, oracle_trace)

        if not step_alignment["all_match"]:
            issues.append("STEP_MISMATCH")
        if step_alignment["missing_steps"]:
            issues.append("MISSING_STEPS")
        if step_alignment["extra_steps"]:
            issues.append("EXTRA_STEPS")
        if step_alignment["reordered_steps"]:
            issues.append("REORDERED_STEPS")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, step_alignment, severity)

        return {
            "lane": "step_correctness",
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
            "prompt": prompt,
            "output": output,
            "trace": trace,
            "oracle_trace": oracle_trace,
            "step_alignment": step_alignment,
        }

    def compare_steps(
        self, trace: List[str], oracle_trace: List[str]
    ) -> Dict[str, Any]:
        all_match = trace == oracle_trace
        missing_steps = [s for s in oracle_trace if s not in trace]
        extra_steps = [s for s in trace if s not in oracle_trace]
        reordered_steps = (
            not all_match and not missing_steps and not extra_steps
        )

        return {
            "all_match": all_match,
            "missing_steps": missing_steps,
            "extra_steps": extra_steps,
            "reordered_steps": reordered_steps,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if "STEP_MISMATCH" in issues:
            return "CRITICAL"
        if "MISSING_STEPS" in issues:
            return "SEVERE"
        if "EXTRA_STEPS" in issues or "REORDERED_STEPS" in issues:
            return "MODERATE"
        return "MINOR"

    def build_explanation(
        self,
        issues: List[str],
        alignment: Dict[str, Any],
        severity: str,
    ) -> str:
        if not issues:
            return "All reasoning steps match the oracle trace."

        parts = [f"Severity: {severity}"]

        if alignment["missing_steps"]:
            parts.append(
                f"Missing steps: {alignment['missing_steps']}"
            )
        if alignment["extra_steps"]:
            parts.append(
                f"Extra steps: {alignment['extra_steps']}"
            )
        if alignment["reordered_steps"]:
            parts.append("Steps are reordered compared to oracle.")

        return " ".join(parts)
