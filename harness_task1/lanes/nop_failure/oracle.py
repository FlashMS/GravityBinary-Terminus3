from typing import Dict, Any


class NopFailureOracle:
    """
    Oracle for NOP failure lane.
    Produces representative NOP / trivial outputs to test the verifier.
    """

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def get_test_cases(self):
        return [
            "",
            "NOP",
            "I cannot solve this",
            "Done",
            "OK",
            "Success",
            "no output",
            "null",
            "undefined",
            "pass",
            "skip",
        ]
