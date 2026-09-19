GravityBinary Terminus3 Evaluation Framework
This repository contains a complete Terminus3 evaluation harness and a fully‑packaged ML evaluation domain + task designed to measure reasoning drift, determinism, hallucination, and output‑format compliance in lightweight reasoning agents.

The project is structured into two major components:

📁 ML_Eval_Domain/task1 — Uploadable Terminus Task
This folder contains the actual Terminus3 task you upload to Snorkel/Terminus for static and dynamic evaluation.

Contents
instruction.md — Human‑readable task description

task.toml — Task metadata

environment/ — Dockerfile + runtime environment

solution/ — Evaluator implementation (solve.sh, Python files, etc.)

tests/ — Deterministic test suite executed during static check

Task Summary
The task evaluates a math‑reasoning agent by detecting reasoning drift, including:

skipped reasoning steps

invented or hallucinated steps

scope changes

inconsistent reasoning traces

The evaluator outputs:

json
{
  "drift": true | false,
  "reasons": ["..."],
  "score": 0.0 – 1.0
}
This task is deterministic: same input → same output.

📁 harness_task1 — Terminus3 Evaluation Cockpit
This folder contains the evaluation harness used for local testing and multi‑lane evaluation.

Key Components
lanes/ — Determinism, hallucination, difficulty, drift, stability, etc.

contracts/ — Input/output schema definitions

eval/ — Lane execution logic

output/ — Generated evaluation artifacts

oracle.py — Reference oracle for correctness checks

This harness is not uploaded to Terminus — it is used locally to validate your task before submission.

📁 EC_execution_framework.txt
Notes describing the deterministic execution framework used to rebuild and validate the cockpit.

📟 Execution (CLI Usage)
These commands are for users running the project, not for your terminal when pasting the README.

bash
# Clone the repository
git clone https://github.com/FlashMS/GravityBinary-Terminus3.git
cd GravityBinary-Terminus3
Run the Uploadable Task
bash
cd ML_Eval_Domain/task1
bash environment/build.sh
bash solution/solve.sh input.json output.json
bash tests/test.sh
Run the Harness
bash
cd harness_task1
python3 eval/run.py
ls output/
Package the Task for Terminus Upload
bash
zip -r ML_Eval_Domain_task1.zip ML_Eval_Domain/task1
📜 License
MIT License recommended.

📣 About
This project is part of GravityBinary’s ongoing work in deterministic evaluation systems, reasoning‑drift detection, and multi‑lane ML agent benchmarking.

⭐ Todd — THIS is the README you paste into GitHub.
Not into WSL.
Not into your terminal.
Not into Bash.

Paste it into GitHub → “Add file” → “Create new file” → README.md → Save.
