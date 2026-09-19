from typing import List, Dict, Any


class MultiRunStabilityOracle:
    """
    Oracle for the Multi-Run Stability lane.
    Ensures that the model produces stable, repeatable outputs across multiple runs.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - expected_answer: the answer that must remain stable across runs
        """
        return [
            {
                "prompt": "What is the capital of Canada?",
                "expected_answer": "Ottawa"
            },
            {
                "prompt": "What is 9 * 9?",
                "expected_answer": "81"
            },
            {
                "prompt": "What gas do plants absorb during photosynthesis?",
                "expected_answer": "Carbon dioxide"
            },
            {
                "prompt": "Who painted the Mona Lisa?",
                "expected_answer": "Leonardo da Vinci"
            },
            {
                "prompt": "What is the largest ocean on Earth?",
                "expected_answer": "Pacific Ocean"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the expected stable answer.
        The evaluator checks whether the model output remains stable across runs.
        """
        return {
            "expected_answer": test_case["expected_answer"]
        }
