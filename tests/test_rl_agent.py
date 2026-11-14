import unittest
from vulnerable_lab_rl.rl_agent import QLearningAgent
from vulnerable_lab_rl.train import evaluate, train

class QLearningTests(unittest.TestCase):
    def test_q_update_moves_value_toward_reward(self):
        agent = QLearningAgent(alpha=0.5, epsilon=0.0)
        state = ("AUTHZ-001", "report")
        agent.update(state, 0, 1.0, None, True)
        self.assertAlmostEqual(agent.q[state][0], 0.5)

    def test_training_learns_finite_synthetic_scenarios(self):
        _, metrics = train(episodes=5000, seed=11)
        self.assertGreaterEqual(metrics["perfect_report_rate"], 0.99)
        self.assertEqual(metrics["episodes"], 300)

    def test_greedy_evaluation_is_deterministic(self):
        agent, _ = train(episodes=5000, seed=13)
        self.assertEqual(evaluate(agent, 5), evaluate(agent, 5))

if __name__ == "__main__":
    unittest.main()
