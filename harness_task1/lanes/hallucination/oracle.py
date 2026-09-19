from typing import List, Dict, Any


class HallucinationOracle:
    """
    Oracle for the Hallucination lane.
    Produces deterministic expected answers for prompts where factual correctness is required.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the question or instruction
        - expected_answer: the factual ground truth
        """
        return [
            {
                "prompt": "What is the capital of France?",
                "expected_answer": "Paris"
            },
            {
                "prompt": "Who wrote the play 'Hamlet'?",
                "expected_answer": "William Shakespeare"
            },
            {
                "prompt": "What is the chemical symbol for water?",
                "expected_answer": "H2O"
            },
            {
                "prompt": "How many continents are there on Earth?",
                "expected_answer": "7"
            },
            {
                "prompt": "What planet is known as the Red Planet?",
                "expected_answer": "Mars"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the factual ground truth.
        The evaluator checks whether the model output matches it.
        """
        return {
            "expected_answer": test_case["expected_answer"]
        }
