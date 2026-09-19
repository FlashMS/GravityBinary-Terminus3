from typing import List, Dict, Any


class DeterminismOracle:
    """
    Oracle for the Determinism lane.
    Produces deterministic expected outputs for prompts that should yield
    the same answer every time (no randomness, no variation).
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - expected_answer: the deterministic ground truth
        """
        return [
            {
                "prompt": "What is 2 + 2?",
                "expected_answer": "4"
            },
            {
                "prompt": "What is the capital of Japan?",
                "expected_answer": "Tokyo"
            },
            {
                "prompt": "What is the square root of 81?",
                "expected_answer": "9"
            },
            {
                "prompt": "What color is the sky on a clear day?",
                "expected_answer": "blue"
            },
            {
                "prompt": "How many days are in a week?",
                "expected_answer": "7"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the deterministic ground truth.
        The evaluator checks whether the model output matches it exactly.
        """
        return {
            "expected_answer": test_case["expected_answer"]
        }
