"""Small episodic environment for synthetic security-analysis tasks."""

from copy import deepcopy
from typing import Any

from .evaluator import score_finding
from .scenarios import SCENARIOS


class SecurityEvaluationEnv:
    """A dependency-free, Gym-like environment for evaluating agent reports.

    Supported actions:
      {"type": "inspect"}
      {"type": "submit", "finding_id": str, "severity": str, "evidence": str}
      {"type": "finish"}

    The environment only presents fictional text and scores reports. It never
    performs security testing against a system.
    """

    def __init__(self) -> None:
        self.scenario_id: str | None = None
        self._done = True
        self._last_observation: dict[str, Any] | None = None

    def reset(self, scenario_id: str = "AUTHZ-001") -> dict[str, Any]:
        if scenario_id not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_id}")
        self.scenario_id = scenario_id
        self._done = False
        scenario = SCENARIOS[scenario_id]
        self._last_observation = {
            "scenario_id": scenario_id,
            "title": scenario["title"],
            "prompt": scenario["prompt"],
            "available_actions": ["inspect", "submit", "finish"],
        }
        return deepcopy(self._last_observation)

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if self._done or self.scenario_id is None:
            raise RuntimeError("Episode is not active. Call reset() first.")
        if not isinstance(action, dict):
            raise TypeError("action must be a dictionary")

        action_type = action.get("type")
        if action_type == "inspect":
            return deepcopy(self._last_observation), 0.0, False, {"status": "inspection_recorded"}

        if action_type == "finish":
            self._done = True
            return {"message": "Episode finished without a submission."}, 0.0, True, {"score": 0}

        if action_type == "submit":
            expected = SCENARIOS[self.scenario_id]["expected"]
            result = score_finding(expected, action)
            self._done = True
            return {"message": "Submission evaluated."}, result["score"] / 100.0, True, result

        raise ValueError("Unsupported action type. Use inspect, submit, or finish.")
