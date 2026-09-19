# Task: Reasoning Drift Evaluation for a Math Solver

You are given a Python script that implements a simple math “reasoning agent”.
The agent receives a word problem, produces a step-by-step reasoning trace, and then outputs a final numeric answer.

Your job is to **implement a drift evaluator** that detects when the agent’s reasoning:
- skips required steps,
- invents steps that are not implied by the problem,
- or changes the scope of the problem (e.g., starts talking about unrelated topics).

You must:

1. Read the agent’s output trace from a JSON file.
2. Compare the trace against a reference “oracle” trace.
3. Decide whether the agent’s reasoning exhibits **reasoning drift**.
4. Output a JSON report with:
   - `drift`: `true` or `false`
   - `reasons`: list of strings explaining the drift
   - `score`: a float between 0 and 1 (1 = no drift, 0 = severe drift)

Constraints:

- Do not modify the agent itself; only implement the evaluator.
- Your evaluator must be **deterministic**: same input → same output.
- Your evaluator must handle at least 10 test cases.
- Your solution must pass the provided tests in `tests/test.sh`.

You will implement your solution in `solution/solve.sh` and any supporting Python files under `solution/`.
