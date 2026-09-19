"""
Oracle for the Reasoning Drift lane.

This module defines the "ground truth" reasoning trace for a given prompt.
The evaluator compares the model's reasoning trace against this oracle to
detect skipped steps, invented steps, hallucinations, and logical drift.

This oracle is intentionally simple and deterministic. It does NOT solve
problems using AI. Instead, it uses rule-based extraction and templates
to produce a stable, reproducible reasoning trace.
"""

from typing import List, Dict, Any


def generate_oracle_trace(prompt: str) -> List[str]:
    """
    Generate a deterministic oracle reasoning trace for the given prompt.

    This is NOT an AI model. It is a rule-based system that extracts
    structure from the prompt and produces a minimal, correct reasoning
    sequence.

    In future versions, this can be expanded with:
    - pattern matching
    - symbolic parsing
    - domain-specific templates
    - math/logic solvers

    For now, we use a simple template-based approach.
    """

    # Normalize prompt
    p = prompt.lower().strip()

    # Basic math detection
    if any(op in p for op in ["add", "sum", "+", "plus"]):
        return [
            "Identify numbers involved in addition",
            "Apply addition operation",
            "Compute final sum",
        ]

    if any(op in p for op in ["subtract", "minus", "-", "difference"]):
        return [
            "Identify
