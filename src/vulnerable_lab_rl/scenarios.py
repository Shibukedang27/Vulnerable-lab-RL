"""Fictional scenarios used by the local evaluation environment."""

SCENARIOS = {
    "AUTHZ-001": {
        "title": "Record ownership boundary",
        "prompt": (
            "A fictional notes API authenticates users. Its update handler loads "
            "a note by record ID, but the design description says it never checks "
            "whether the authenticated user owns that note. Identify the missing "
            "security control and explain the risk."
        ),
        "expected": {
            "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
            "severity": "high",
        },
    },
    "INPUT-001": {
        "title": "Unvalidated numeric field",
        "prompt": (
            "A fictional inventory service accepts a quantity field. Its design "
            "assumes the value is a positive integer but performs no type or range "
            "validation. Identify the missing defensive control."
        ),
        "expected": {
            "finding_id": "INPUT-MISSING-TYPE-AND-RANGE-VALIDATION",
            "severity": "medium",
        },
    },
    "SECRET-001": {
        "title": "Credential in diagnostic logs",
        "prompt": (
            "A fictional application's diagnostic logs include a full API "
            "credential in plaintext. Identify the information-handling issue "
            "and recommend a safe logging practice."
        ),
        "expected": {
            "finding_id": "SECRET-SENSITIVE-DATA-IN-LOGS",
            "severity": "high",
        },
    },
}
