import unittest

from vulnerable_lab_rl.evaluator import score_finding


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
            "severity": "high",
        }

    def test_perfect_submission(self):
        result = score_finding(self.expected, {
            **self.expected,
            "evidence": "The design omits a record ownership check.",
        })
        self.assertEqual(result["score"], 100)

    def test_wrong_severity(self):
        result = score_finding(self.expected, {
            "finding_id": self.expected["finding_id"],
            "severity": "low",
            "evidence": "The design omits a record ownership check.",
        })
        self.assertEqual(result["score"], 80)

    def test_missing_identifier(self):
        result = score_finding(self.expected, {
            "finding_id": "OTHER",
            "severity": "high",
            "evidence": "The design omits a record ownership check.",
        })
        self.assertEqual(result["score"], 40)


if __name__ == "__main__":
    unittest.main()
