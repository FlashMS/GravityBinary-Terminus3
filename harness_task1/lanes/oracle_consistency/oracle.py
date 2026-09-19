from typing import List, Dict, Any


class OracleConsistencyOracle:
    """
    Oracle for the Oracle Consistency lane.
    Ensures that the model produces consistent answers across repeated identical prompts.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - expected_answer: the answer that must remain consistent across runs
        """
        return [
            {
                "prompt": "What is the capital of Italy?",
                "expected_answer": "Rome"
            },
            {
                "prompt": "What is 10 + 5?",
                "expected_answer": "15"
            },
            {
                "prompt": "What is the boiling point of water in Celsius?",
                "expected_answer": "100"
            },
            {
                "prompt": "Who wrote '1984'?",
                "expected_answer": "George Orwell"
            },
            {
                "prompt": "What planet is closest to the Sun?",
                "expected_answer": "Mercury"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the expected answer.
        The evaluator checks whether the model output matches it consistently.
        """
        return {
            "expected_answer": test_case["expected_answer"]
        }
