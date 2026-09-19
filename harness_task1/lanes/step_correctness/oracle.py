from typing import List, Dict, Any


class StepCorrectnessOracle:
    """
    Oracle for the Step Correctness lane.
    Produces deterministic step-by-step reasoning traces for arithmetic prompts.
    The evaluator checks whether the model's reasoning steps match the oracle steps.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - steps: the correct step-by-step reasoning trace
        """
        return [
            {
                "prompt": "Compute 5 + 7.",
                "steps": ["Identify numbers 5 and 7", "Apply addition", "Compute 12"]
            },
            {
                "prompt": "Compute 20 - 4.",
                "steps": ["Identify numbers 20 and 4", "Apply subtraction", "Compute 16"]
            },
            {
                "prompt": "Compute 6 * 3.",
                "steps": ["Identify numbers 6 and 3", "Apply multiplication", "Compute 18"]
            },
            {
                "prompt": "Compute 100 / 5.",
                "steps": ["Identify numbers 100 and 5", "Apply division", "Compute 20"]
            },
            {
                "prompt": "If you have 3 apples and buy 2 more, how many apples do you have?",
                "steps": ["Identify quantities 3 and 2", "Apply addition", "Compute 5"]
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the correct reasoning steps.
        The evaluator checks whether the model's reasoning matches them.
        """
        return {
            "expected_steps": test_case["steps"]
        }
