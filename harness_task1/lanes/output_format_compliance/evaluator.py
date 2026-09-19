from typing import Dict, Any, List
import json
import os


class OutputFormatComplianceEvaluator:
    """
    Validates JSON report format across all lanes.
    Ensures required keys exist and types are correct.
    """

    REQUIRED_KEYS = [
        "lane",
        "severity",
        "prompt",
        "explanation",
    ]

    def __init__(self, contract: Dict[str, Any]):
        self.contract = contract

    def evaluate_file(self, path: str) -> Dict[str, Any]:
        issues = []

        try:
            with open(path, "r") as f:
                report = json.load(f)
        except Exception:
            return {
                "file": path,
                "issues": ["INVALID_JSON"],
                "severity": "CRITICAL",
                "explanation": "File is not valid JSON.",
            }

        # Required keys
        for key in self.REQUIRED_KEYS:
            if key not in report:
                issues.append(f"MISSING_KEY_{key.upper()}")

        # Type checks
        if "severity" in report and not isinstance(report["severity"], str):
            issues.append("INVALID_TYPE_SEVERITY")

        if "prompt" in report and not isinstance(report["prompt"], str):
            issues.append("INVALID_TYPE_PROMPT")

        severity = self.classify_severity(issues)
        explanation = self.build_explanation(issues, severity)

        return {
            "file": path,
            "issues": issues,
            "severity": severity,
            "explanation": explanation,
        }

    def classify_severity(self, issues: List[str]) -> str:
        if not issues:
            return "NONE"
        if any("MISSING_KEY" in i for i in issues):
            return "CRITICAL"
        if "INVALID_JSON" in issues:
            return "CRITICAL"
        return "MINOR"

    def build_explanation(self, issues: List[str], severity: str) -> str:
        if not issues:
            return "Report format is fully compliant."
        return f"Severity: {severity}. Issues: {', '.join(issues)}."
