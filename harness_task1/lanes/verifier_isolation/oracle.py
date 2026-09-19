from typing import List, Dict, Any


class VerifierIsolationOracle:
    """
    Oracle for the Verifier Isolation lane.
    Ensures that the model does NOT leak reasoning steps or chain-of-thought
    when the prompt explicitly forbids it.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - expected_behavior: the correct isolated (no reasoning) output
        """
        return [
            {
                "prompt": "Give the final answer only: What is 8 + 5?",
                "expected_behavior": "13"
            },
            {
                "prompt": "Final answer only: What is the capital of Germany?",
                "expected_behavior": "Berlin"
            },
            {
                "prompt": "Do not show your steps. What is 12 * 3?",
                "expected_behavior": "36"
            },
            {
                "prompt": "Answer only: Who wrote 'The Hobbit'?",
                "expected_behavior": "J.R.R. Tolkien"
            },
            {
                "prompt": "Final answer only: What planet is known as the Red Planet?",
                "expected_behavior": "Mars"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the isolated final answer.
        The evaluator checks whether the model leaks reasoning.
        """
        return {
            "expected_answer": test_case["expected_behavior"]
        }
