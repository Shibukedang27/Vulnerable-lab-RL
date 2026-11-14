import unittest

from vulnerable_lab_rl.environment import SecurityEvaluationEnv


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.env = SecurityEvaluationEnv()

    def test_reset_returns_observation(self):
        observation = self.env.reset("AUTHZ-001")
        self.assertEqual(observation["scenario_id"], "AUTHZ-001")
        self.assertIn("prompt", observation)

    def test_inspect_keeps_episode_active(self):
        self.env.reset()
        _, reward, done, info = self.env.step({"type": "inspect"})
        self.assertEqual(reward, 0.0)
        self.assertFalse(done)
        self.assertEqual(info["status"], "inspection_recorded")

    def test_correct_submission_gets_full_reward(self):
        self.env.reset("AUTHZ-001")
        _, reward, done, info = self.env.step({
            "type": "submit",
            "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
            "severity": "high",
            "evidence": "The handler does not verify record ownership for the authenticated user.",
        })
        self.assertEqual(reward, 1.0)
        self.assertTrue(done)
        self.assertEqual(info["score"], 100)

    def test_unknown_scenario_rejected(self):
        with self.assertRaises(ValueError):
            self.env.reset("UNKNOWN")

    def test_step_after_done_rejected(self):
        self.env.reset()
        self.env.step({"type": "finish"})
        with self.assertRaises(RuntimeError):
            self.env.step({"type": "inspect"})


if __name__ == "__main__":
    unittest.main()
