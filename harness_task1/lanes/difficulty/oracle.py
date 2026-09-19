from typing import List, Dict, Any


class DifficultyOracle:
    """
    Oracle for the Difficulty lane.
    Produces deterministic difficulty classifications for prompts.
    The evaluator checks whether the model assigns the correct difficulty level.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Each test case includes:
        - prompt: the instruction given to the model
        - difficulty: expected difficulty classification
        """
        return [
            {
                "prompt": "What is 3 + 4?",
                "difficulty": "easy"
            },
            {
                "prompt": "Explain photosynthesis in one paragraph.",
                "difficulty": "medium"
            },
            {
                "prompt": "Prove the Pythagorean theorem.",
                "difficulty": "hard"
            },
            {
                "prompt": "Summarize the plot of 'War and Peace'.",
                "difficulty": "medium"
            },
            {
                "prompt": "Solve the integral ∫ x^2 * sin(x) dx.",
                "difficulty": "hard"
            }
        ]

    def generate_expected_behavior(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        The oracle returns the expected difficulty classification.
        The evaluator checks whether the model matches it.
        """
        return {
            "expected_difficulty": test_case["difficulty"]
        }
