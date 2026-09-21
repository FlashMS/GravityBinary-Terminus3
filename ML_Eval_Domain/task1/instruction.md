# Task Instructions

The evaluator must read the input trace and oracle reference provided by the agent and determine whether drift is present. The evaluator must operate deterministically and produce a JSON report describing the result.

## Inputs

- `/task/tests/cases.json`: A JSON file containing the input cases the evaluator must process.
- `/task/solution/solve.sh`: The agent’s solution script, which produces the output to be evaluated.
- `/task/tests/output.json`: The expected output format and structure.

## Required Behavior

The evaluator must:

- Execute the agent’s solution script.
- Read the agent-produced output.
- Compare the output against the oracle reference.
- Determine whether drift exists based on the comparison rules defined in the test suite.
- Produce a JSON report containing:
  - Whether drift was detected.
  - Any mismatches found.
  - Any additional diagnostic information required by the test suite.

## Output

The evaluator must write its final JSON report to standard output. The report must match the structure defined in `/task/tests/output.json`.

## Constraints

- The evaluator must run deterministically.
- The evaluator must not access the network.
- The evaluator must complete within the timeout specified in `task.toml`.
