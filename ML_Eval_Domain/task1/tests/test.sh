#!/usr/bin/env bash
set -euo pipefail

TASK_ROOT="."
INPUT="${TASK_ROOT}/tests/cases.json"
OUTPUT="${TASK_ROOT}/tests/output.json"
cat "${INPUT}" | "${TASK_ROOT}/solution/solve.sh" > "${OUTPUT}"

python - << 'PYCODE'
import json, sys

with open("/task/tests/output.json") as f:
    out = json.load(f)

results = out["results"]
if len(results) < 10:
    print("FAIL: expected at least 10 cases")
    sys.exit(1)

if not any(r["drift"] for r in results):
    print("FAIL: expected at least one drift-positive case")
    sys.exit(1)

print("OK: tests passed")
PYCODE
