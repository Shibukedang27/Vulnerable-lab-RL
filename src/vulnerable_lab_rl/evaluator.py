"""Transparent scoring for structured findings in synthetic scenarios."""

from typing import Any


def score_finding(expected: dict[str, str], submitted: dict[str, Any]) -> dict[str, Any]:
    """Score one finding out of 100 using a simple, documented rubric.

    60 points: exact finding identifier.
    20 points: evidence is a non-empty string of at least 20 characters.
    20 points: severity matches the expected severity.

    This baseline does not semantically validate evidence.
    """
    score = 0
    id_match = submitted.get("finding_id") == expected["finding_id"]
    severity_match = submitted.get("severity") == expected["severity"]
    evidence = submitted.get("evidence")
    evidence_present = isinstance(evidence, str) and len(evidence.strip()) >= 20

    if id_match:
        score += 60
    if evidence_present:
        score += 20
    if severity_match:
        score += 20

    return {
        "score": score,
        "finding_id_match": id_match,
        "severity_match": severity_match,
        "evidence_present": evidence_present,
        "max_score": 100,
    }
