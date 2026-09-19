import sys
import os
import json
import yaml
from typing import Dict, Any, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from lanes.reasoning_drift.evaluator import ReasoningDriftEvaluator
from lanes.reasoning_drift.oracle import oracle_api
from lanes.reasoning_drift.report import (
    generate_text_report,
    generate_json_report,
    save_text_report,
    save_json_report,
)

from lanes.constraint_adherence.evaluator import ConstraintAdherenceEvaluator
from lanes.constraint_adherence.oracle import oracle_api as ca_oracle
from lanes.constraint_adherence.report import (
    generate_text_report as ca_text_report,
    generate_json_report as ca_json_report,
    save_text_report as ca_save_text,
    save_json_report as ca_save_json,
)

from lanes.hallucination.evaluator import HallucinationEvaluator
from lanes.hallucination.oracle import oracle_api as h_oracle
from lanes.hallucination.report import (
    generate_text_report as h_text_report,
    generate_json_report as h_json_report,
    save_text_report as h_save_text,
    save_json_report as h_save_json,
)

from lanes.determinism.evaluator import DeterminismEvaluator
from lanes.determinism.oracle import oracle_api as d_oracle
from lanes.determinism.report import (
    generate_text_report as d_text_report,
    generate_json_report as d_json_report,
    save_text_report as d_save_text,
    save_json_report as d_save_json,
)

from lanes.step_correctness.evaluator import StepCorrectnessEvaluator
from lanes.step_correctness.oracle import oracle_api as sc_oracle
from lanes.step_correctness.report import (
    generate_text_report as sc_text_report,
    generate_json_report as sc_json_report,
    save_text_report as sc_save_text,
    save_json_report as sc_save_json,
)

from lanes.difficulty.evaluator import DifficultyEvaluator
from lanes.difficulty.oracle import oracle_api as diff_oracle
from lanes.difficulty.report import (
    generate_text_report as diff_text_report,
    generate_json_report as diff_json_report,
    save_text_report as diff_save_text,
    save_json_report as diff_save_json,
)

from lanes.oracle_consistency.evaluator import OracleConsistencyEvaluator
from lanes.oracle_consistency.oracle import oracle_api as oc_oracle
from lanes.oracle_consistency.report import (
    generate_text_report as oc_text_report,
    generate_json_report as oc_json_report,
    save_text_report as oc_save_text,
    save_json_report as oc_save_json,
)

from lanes.verifier_isolation.evaluator import VerifierIsolationEvaluator
from lanes.verifier_isolation.oracle import verifier_api
from lanes.verifier_isolation.report import (
    generate_text_report as vi_text_report,
    generate_json_report as vi_json_report,
    save_text_report as vi_save_text,
    save_json_report as vi_save_json,
)

from lanes.multi_run_stability.evaluator import MultiRunStabilityEvaluator
from lanes.multi_run_stability.oracle import solver_api
from lanes.multi_run_stability.report import (
    generate_text_report as mrs_text_report,
    generate_json_report as mrs_json_report,
    save_text_report as mrs_save_text,
    save_json_report as mrs_save_json,
)


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    tests = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                tests.append(json.loads(line))
    return tests


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def run_reasoning_drift_eval() -> None:
    print("=== Running Reasoning Drift Lane Evaluation ===")
    contract = load_yaml("contracts/reasoning_drift.yaml")
    tests = load_jsonl("lanes/reasoning_drift/tests.jsonl")
    output_dir = "output/reasoning_drift"
    evaluator = ReasoningDriftEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        model_output = "This is a placeholder model output."
        model_trace = ["Read prompt", "Identify operation", "Compute answer"]
        oracle_trace = oracle_api(prompt, model_trace)["oracle_trace"]
        result = evaluator.evaluate(prompt, model_output, model_trace, oracle_trace, [])
        save_text_report(result, f"{output_dir}/test_{test_id}.txt")
        save_json_report(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_constraint_adherence_eval() -> None:
    print("=== Running Constraint Adherence Lane Evaluation ===")
    contract = load_yaml("contracts/constraint_adherence.yaml")
    tests = load_jsonl("lanes/constraint_adherence/tests.jsonl")
    output_dir = "output/constraint_adherence"
    evaluator = ConstraintAdherenceEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        model_output = "42"
        model_trace = ["Read prompt", "Compute answer"]
        oracle_trace = ca_oracle(prompt, model_trace)["oracle_trace"]
        result = evaluator.evaluate(prompt, model_output, model_trace, oracle_trace)
        ca_save_text(result, f"{output_dir}/test_{test_id}.txt")
        ca_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_hallucination_eval() -> None:
    print("=== Running Hallucination Lane Evaluation ===")
    contract = load_yaml("contracts/hallucination.yaml")
    tests = load_jsonl("lanes/hallucination/tests.jsonl")
    output_dir = "output/hallucination"
    evaluator = HallucinationEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        model_output = "42"
        model_trace = ["Read prompt", "Compute answer"]
        oracle_trace = h_oracle(prompt, model_trace)["oracle_trace"]
        result = evaluator.evaluate(prompt, model_output, model_trace, oracle_trace)
        h_save_text(result, f"{output_dir}/test_{test_id}.txt")
        h_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_determinism_eval() -> None:
    print("=== Running Determinism Lane Evaluation ===")
    contract = load_yaml("contracts/determinism.yaml")
    tests = load_jsonl("lanes/determinism/tests.jsonl")
    output_dir = "output/determinism"
    evaluator = DeterminismEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        outputs = ["42", "42", "42"]
        traces = [
            ["Read prompt", "Compute answer"],
            ["Read prompt", "Compute answer"],
            ["Read prompt", "Compute answer"],
        ]
        oracle_trace = d_oracle(prompt, traces[0])["oracle_trace"]
        result = evaluator.evaluate(prompt, outputs, traces, oracle_trace)
        d_save_text(result, f"{output_dir}/test_{test_id}.txt")
        d_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_step_correctness_eval() -> None:
    print("=== Running Step Correctness Lane Evaluation ===")
    contract = load_yaml("contracts/step_correctness.yaml")
    tests = load_jsonl("lanes/step_correctness/tests.jsonl")
    output_dir = "output/step_correctness"
    evaluator = StepCorrectnessEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        model_output = "42"
        model_trace = [
            "Read prompt",
            "Identify operation",
            "Compute answer",
            "Verify result",
        ]
        oracle_trace = sc_oracle(prompt, model_trace)["oracle_trace"]
        result = evaluator.evaluate(prompt, model_output, model_trace, oracle_trace)
        sc_save_text(result, f"{output_dir}/test_{test_id}.txt")
        sc_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_difficulty_eval() -> None:
    print("=== Running Difficulty Lane Evaluation ===")
    contract = load_yaml("contracts/difficulty.yaml")
    tests = load_jsonl("lanes/difficulty/tests.jsonl")
    output_dir = "output/difficulty"
    evaluator = DifficultyEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        oracle_output = diff_oracle(prompt)["oracle_output"]
        solver_outputs = ["42", "41", "42", "40", "42", "39", "42", "38"]
        result = evaluator.evaluate(prompt, solver_outputs, oracle_output)
        diff_save_text(result, f"{output_dir}/test_{test_id}.txt")
        diff_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_oracle_consistency_eval() -> None:
    print("=== Running Oracle Consistency Lane Evaluation ===")
    contract = load_yaml("contracts/oracle_consistency.yaml")
    tests = load_jsonl("lanes/oracle_consistency/tests.jsonl")
    output_dir = "output/oracle_consistency"
    evaluator = OracleConsistencyEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        oracle_outputs = []
        oracle_traces = []
        for _ in range(contract.get("runs", 3)):
            res = oc_oracle(prompt)
            oracle_outputs.append(res["oracle_output"])
            oracle_traces.append(res["oracle_trace"])
        result = evaluator.evaluate(prompt, oracle_outputs, oracle_traces)
        oc_save_text(result, f"{output_dir}/test_{test_id}.txt")
        oc_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_verifier_isolation_eval() -> None:
    print("=== Running Verifier Isolation Lane Evaluation ===")
    contract = load_yaml("contracts/verifier_isolation.yaml")
    tests = load_jsonl("lanes/verifier_isolation/tests.jsonl")
    output_dir = "output/verifier_isolation"
    evaluator = VerifierIsolationEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        solver_outputs = ["42", "41", "40"]
        verifier_decisions = []
        for out in solver_outputs:
            res = verifier_api(prompt, out)
            verifier_decisions.append(res["decision"])
        result = evaluator.evaluate(prompt, solver_outputs, verifier_decisions)
        vi_save_text(result, f"{output_dir}/test_{test_id}.txt")
        vi_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


def run_multi_run_stability_eval() -> None:
    print("=== Running Multi-Run Stability Lane Evaluation ===")
    contract = load_yaml("contracts/multi_run_stability.yaml")
    tests = load_jsonl("lanes/multi_run_stability/tests.jsonl")
    output_dir = "output/multi_run_stability"
    evaluator = MultiRunStabilityEvaluator(contract)
    ensure_dir(output_dir)
    for test in tests:
        test_id = test["id"]
        prompt = test["prompt"]
        solver_outputs = []
        solver_traces = []
        for _ in range(contract.get("runs", 5)):
            res = solver_api(prompt)
            solver_outputs.append(res["output"])
            solver_traces.append(res["trace"])
        result = evaluator.evaluate(prompt, solver_outputs, solver_traces)
        mrs_save_text(result, f"{output_dir}/test_{test_id}.txt")
        mrs_save_json(result, f"{output_dir}/test_{test_id}.json")
        print(f"Saved reports for test {test_id}.")


if __name__ == "__main__":
    run_reasoning_drift_eval()
    run_constraint_adherence_eval()
    run_hallucination_eval()
    run_determinism_eval()
    run_step_correctness_eval()
    run_difficulty_eval()
    run_oracle_consistency_eval()
    run_verifier_isolation_eval()
    run_multi_run_stability_eval()
