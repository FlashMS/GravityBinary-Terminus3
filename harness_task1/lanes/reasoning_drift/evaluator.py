from typing import Dict, Any, List


class ReasoningDriftEvaluator:
    """
    Evaluator for the Reasoning Drift lane.
    Checks whether the model's reasoning remains consistent with the oracle.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def evaluate(self, test: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cockpit-compatible evaluation function.
        The runner passes a single test dict containing:
        - prompt
        - expected_behavior
        """

        prompt = test["prompt"]

        # Placeholder model output until you integrate a real model
        model_output = "This is a placeholder model output."
        model_trace = ["Read prompt", "Identify operation", "Compute answer"]

        # Oracle expected behavior
        expected = test["expected_behavior"]

        # Compare model output to oracle
        is_match = (model_output == expected)

        return {
            "prompt": prompt,
            "model_output": model_output,
            "model_trace": model_trace,
            "expected_behavior": expected,
            "match": is_match
        }
