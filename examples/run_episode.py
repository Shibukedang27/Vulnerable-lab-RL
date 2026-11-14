"""Minimal example of an agent interacting with the environment."""

from vulnerable_lab_rl import SCENARIOS, SecurityEvaluationEnv


env = SecurityEvaluationEnv()
observation = env.reset("INPUT-001")
print(observation["prompt"])

# A sample agent report for this fictional scenario.
expected = SCENARIOS["INPUT-001"]["expected"]
next_observation, reward, done, metrics = env.step({
    "type": "submit",
    **expected,
    "evidence": "The service needs type and range checks to enforce positive integer quantities.",
})

print({"reward": reward, "done": done, "metrics": metrics})
