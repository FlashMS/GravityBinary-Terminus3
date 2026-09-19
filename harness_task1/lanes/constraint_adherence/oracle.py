import json
import os

def load_jsonl(path):
    tests = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                tests.append(json.loads(line))
    return tests

class ConstraintAdherenceOracle:
    def __init__(self, contract):
        self.contract = contract

    def get_test_cases(self):
        return load_jsonl("lanes/constraint_adherence/tests.jsonl")

    def generate_expected_behavior(self, test_case):
        # The evaluator expects this key to exist.
        return {"expected_behavior": "number_only"}
