import json
import os
from typing import Dict, Any

# === Lane Imports ===
from lanes.reasoning_drift.oracle import ReasoningDriftOracle
from lanes.reasoning_drift.evaluator import ReasoningDriftEvaluator
from lanes.reasoning_drift.report import save_report as save_reasoning_report

from lanes.constraint_adherence.oracle import ConstraintAdherenceOracle
from lanes.constraint_adherence.evaluator import ConstraintAdherenceEvaluator
from lanes.constraint_adherence.report import save_report as save_constraint_report

from lanes.hallucination.oracle import HallucinationOracle
from lanes.hallucination.evaluator import HallucinationEvaluator
from lanes.hallucination.report import save_report as save_hallucination_report

from lanes.determinism.oracle import DeterminismOracle
from lanes.determinism.evaluator import DeterminismEvaluator
from lanes.determinism.report import save_report as save_determinism_report

from lanes.step_correctness.oracle import StepCorrectnessOracle
from lanes.step_correctness.evaluator import StepCorrectnessEvaluator
from lanes.step_correctness.report import save_report as save_step_report

from lanes.difficulty.oracle import DifficultyOracle
from lanes.difficulty.evaluator import DifficultyEvaluator
from lanes.difficulty.report import save_report as save_difficulty_report

from lanes.oracle_consistency.oracle import OracleConsistencyOracle
from lanes.oracle_consistency.evaluator import OracleConsistencyEvaluator
from lanes.oracle_consistency.report import save_report as save_oracle_consistency_report

from lanes.verifier_isolation.oracle import VerifierIsolationOracle
from lanes.verifier_isolation.evaluator import VerifierIsolationEvaluator
from lanes.verifier_isolation.report import save_report as save_verifier_isolation_report

from lanes.multi_run_stability.oracle import MultiRunStabilityOracle
from lanes.multi_run_stability.evaluator import MultiRunStabilityEvaluator
from lanes.multi_run_stability.report import save_report as save_multi_run_report

from lanes.output_format_compliance.oracle import OutputFormatComplianceOracle
from lanes.output_format_compliance.evaluator import OutputFormatComplianceEvaluator
from lanes.output_format_compliance.report import save_report as save_output_format_report


# === Contract Loader ===
def load_contract(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


# === Corrected run_lane (your patched version) ===

def run_lane(contract_path, OracleClass, EvaluatorClass, save_report, lane_name):
    contract = load_contract(contract_path)
    oracle = OracleClass(contract)
    evaluator = EvaluatorClass(contract)

    output_dir = os.path.join("output", lane_name)
    os.makedirs(output_dir, exist_ok=True)

    # SPECIAL CASE: Output Format Compliance
    if not hasattr(oracle, "get_test_cases"):
        idx = 1
        # Scan all lane output directories
        for root, dirs, files in os.walk("output"):
            for file in files:
                if file.endswith(".json"):
                    path = os.path.join(root, file)
                    try:
                        result = evaluator.evaluate_file(path)
                        save_report(output_dir, idx, result)
                        idx += 1
                    except Exception as e:
                        # Save error report
                        save_report(output_dir, idx, {"error": str(e), "file": path})
                        idx += 1
        return

    idx = 1
    for test_case in oracle.get_test_cases():
        expected = oracle.generate_expected_behavior(test_case)

        model_output = "42"
        model_trace = ["Model read prompt", "Model produced output"]

        if hasattr(oracle, "generate_oracle_trace"):
            oracle_result = oracle.generate_oracle_trace(test_case, model_trace)
            oracle_trace = oracle_result.get("oracle_trace", [])
            oracle_output = oracle_result.get("oracle_output", "oracle_default")
        else:
            oracle_trace = ["Oracle executed"]
            oracle_output = "oracle_default"

        test_dict = {
            "prompt": test_case["prompt"],
            "expected_behavior": expected.get("expected_behavior"),
            "output": model_output,
            "trace": model_trace,
            "oracle_trace": oracle_trace,
            "oracle_output": oracle_output
        }

        try:
            result = evaluator.evaluate(test_dict)
        except TypeError:
            try:
                result = evaluator.evaluate(
                    prompt=test_dict["prompt"],
                    output=test_dict["output"],
                    trace=test_dict["trace"],
                    oracle_trace=test_dict["oracle_trace"]
                )
            except TypeError:
                try:
                    outputs = [model_output, model_output, model_output]
                    traces = [model_trace, model_trace, model_trace]

                    result = evaluator.evaluate(
                        prompt=test_dict["prompt"],
                        outputs=outputs,
                        traces=traces,
                        oracle_trace=test_dict["oracle_trace"]
                    )
                except TypeError:
                    try:
                        solver_outputs = [model_output, model_output]
                        result = evaluator.evaluate(
                            prompt=test_dict["prompt"],
                            solver_outputs=solver_outputs,
                            oracle_output=test_dict["oracle_output"]
                        )
                    except TypeError:
                        try:
                            oracle_outputs = [oracle_output, oracle_output]
                            oracle_traces = [oracle_trace, oracle_trace]

                            result = evaluator.evaluate(
                                prompt=test_dict["prompt"],
                                oracle_outputs=oracle_outputs,
                                oracle_traces=oracle_traces
                            )
                        except TypeError:
                            try:
                                solver_outputs = [model_output, model_output]
                                verifier_decisions = ["accept", "accept"]

                                result = evaluator.evaluate(
                                    prompt=test_dict["prompt"],
                                    solver_outputs=solver_outputs,
                                    verifier_decisions=verifier_decisions
                                )
                            except TypeError:
                                solver_outputs = [model_output, model_output, model_output]
                                solver_traces = [model_trace, model_trace, model_trace]

                                result = evaluator.evaluate(
                                    prompt=test_dict["prompt"],
                                    solver_outputs=solver_outputs,
                                    solver_traces=solver_traces
                                )

        save_report(output_dir, idx, result)
        idx += 1


# === Main Cockpit Runner ===
def main():
    print("=== Running Reasoning Drift Lane Evaluation ===")
    run_lane(
        "contracts/reasoning_drift.json",
        ReasoningDriftOracle,
        ReasoningDriftEvaluator,
        save_reasoning_report,
        "reasoning_drift"
    )

    print("=== Running Constraint Adherence Lane Evaluation ===")
    run_lane(
        "contracts/constraint_adherence.json",
        ConstraintAdherenceOracle,
        ConstraintAdherenceEvaluator,
        save_constraint_report,
        "constraint_adherence"
    )

    print("=== Running Hallucination Lane Evaluation ===")
    run_lane(
        "contracts/hallucination.json",
        HallucinationOracle,
        HallucinationEvaluator,
        save_hallucination_report,
        "hallucination"
    )

    print("=== Running Determinism Lane Evaluation ===")
    run_lane(
        "contracts/determinism.json",
        DeterminismOracle,
        DeterminismEvaluator,
        save_determinism_report,
        "determinism"
    )

    print("=== Running Step Correctness Lane Evaluation ===")
    run_lane(
        "contracts/step_correctness.json",
        StepCorrectnessOracle,
        StepCorrectnessEvaluator,
        save_step_report,
        "step_correctness"
    )

    print("=== Running Difficulty Lane Evaluation ===")
    run_lane(
        "contracts/difficulty.json",
        DifficultyOracle,
        DifficultyEvaluator,
        save_difficulty_report,
        "difficulty"
    )

    print("=== Running Oracle Consistency Lane Evaluation ===")
    run_lane(
        "contracts/oracle_consistency.json",
        OracleConsistencyOracle,
        OracleConsistencyEvaluator,
        save_oracle_consistency_report,
        "oracle_consistency"
    )

    print("=== Running Verifier Isolation Lane Evaluation ===")
    run_lane(
        "contracts/verifier_isolation.json",
        VerifierIsolationOracle,
        VerifierIsolationEvaluator,
        save_verifier_isolation_report,
        "verifier_isolation"
    )

    print("=== Running Multi-Run Stability Lane Evaluation ===")
    run_lane(
        "contracts/multi_run_stability.json",
        MultiRunStabilityOracle,
        MultiRunStabilityEvaluator,
        save_multi_run_report,
        "multi_run_stability"
    )

    print("=== Running Output Format Compliance Lane Evaluation ===")
    run_lane(
        "contracts/output_format_compliance.json",
        OutputFormatComplianceOracle,
        OutputFormatComplianceEvaluator,
        save_output_format_report,
        "output_format_compliance"
    )


if __name__ == "__main__":
    main()
