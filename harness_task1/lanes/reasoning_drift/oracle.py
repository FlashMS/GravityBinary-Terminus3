from typing import List, Dict, Any


class ReasoningDriftOracle:
    """
    Oracle for the Reasoning Drift lane.
    Ensures that the model's reasoning does not drift between runs.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - expected_behavior: the correct answer that should not drift
        """
        return [
            {
                "prompt": "What is 2 + 2?",
                "expected_behavior": "4"
            },
            {
                "prompt": "What is the capital of France?",
                "expected_behavior": "Paris"
            },
            {
                "prompt": "What is the boiling point of water in Celsius?",
                "expected_behavior": "100"
            },
            {
                "prompt": "Who wrote 'Pride and Prejudice'?",
                "expected_behavior": "Jane Austen"
            },
            {
                "prompt": "What planet is known as the Red Planet?",
                "expected_behavior": "Mars"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the expected answer.
        The evaluator checks whether the model output matches it consistently.
        """
        return {
            "expected_behavior": test_case["expected_behavior"]
        }
