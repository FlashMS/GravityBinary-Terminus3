from typing import Dict, Any, List


class DifficultyEvaluator:
    """
    Measures difficulty by simulating multiple solver runs
    and counting how many times the solver fails.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract
        self.runs = contract.get("runs", 8)
        self.required_failures = contract.get("required_failures", 3)

    def evaluate(
        self,
        prompt: str,
        solver_outputs: List[str],
        oracle_output: str,
    ) -> Dict[str, Any]:

        failures = sum(1 for out in solver_outputs if out != oracle_output)
        passes = self.runs - failures

        meets_threshold = failures >= self.required_failures

        return {
            "lane": "difficulty",
            "prompt": prompt,
            "oracle_output": oracle_output,
            "solver_outputs": solver_outputs,
            "runs": self.runs,
            "failures": failures,
            "passes": passes,
            "required_failures": self.required_failures,
            "meets_threshold": meets_threshold,
            "severity": self.classify_severity(meets_threshold),
            "explanation": self.build_explanation(failures, meets_threshold),
        }

    def classify_severity(self, meets_threshold: bool) -> str:
        if meets_threshold:
            return "NONE"
        return "CRITICAL"

    def build_explanation(self, failures: int, meets_threshold: bool) -> str:
        if meets_threshold:
            return (
                f"Difficulty threshold met: solver failed {failures} times."
            )
        return (
            f"Difficulty threshold NOT met: solver failed only {failures} times."
        )
