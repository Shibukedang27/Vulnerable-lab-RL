"""Tabular Q-learning agent for the synthetic security-evaluation environment."""
from __future__ import annotations
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Hashable

@dataclass(frozen=True)
class CandidateAction:
    finding_id: str
    severity: str
    evidence: str
    def as_dict(self) -> dict[str, str]:
        return {"type": "submit", "finding_id": self.finding_id, "severity": self.severity, "evidence": self.evidence}

# Finite synthetic report choices only; no exploit payloads or target actions.
CANDIDATES = (
    CandidateAction("AUTHZ-MISSING-OWNERSHIP-CHECK", "high", "The design does not verify record ownership for the authenticated user."),
    CandidateAction("INPUT-MISSING-TYPE-AND-RANGE-VALIDATION", "medium", "The service needs type and range validation for the quantity field."),
    CandidateAction("SECRET-SENSITIVE-DATA-IN-LOGS", "high", "The diagnostic logs expose a credential and should redact sensitive values."),
    CandidateAction("AUTHZ-MISSING-OWNERSHIP-CHECK", "medium", "The design does not verify record ownership for the authenticated user."),
    CandidateAction("INPUT-MISSING-TYPE-AND-RANGE-VALIDATION", "high", "The service needs type and range validation for the quantity field."),
    CandidateAction("SECRET-SENSITIVE-DATA-IN-LOGS", "low", "The diagnostic logs expose a credential and should redact sensitive values."),
    CandidateAction("GENERIC-SECURITY-CONCERN", "low", "The scenario suggests a general security concern that needs review."),
)

class QLearningAgent:
    """Epsilon-greedy tabular Q learner for scenario/report states."""
    def __init__(self, actions=CANDIDATES, alpha=0.2, gamma=0.9, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.995, seed=7):
        self.actions, self.alpha, self.gamma = actions, alpha, gamma
        self.epsilon, self.epsilon_min, self.epsilon_decay = epsilon, epsilon_min, epsilon_decay
        self.rng = random.Random(seed)
        self.q = defaultdict(lambda: [0.0] * len(actions))
    def choose_action(self, state, explore=True):
        if explore and self.rng.random() < self.epsilon:
            return self.rng.randrange(len(self.actions))
        values = self.q[state]
        best = max(values)
        return self.rng.choice([i for i, value in enumerate(values) if value == best])
    def update(self, state, action_index, reward, next_state, done):
        old = self.q[state][action_index]
        future = 0.0 if done or next_state is None else max(self.q[next_state])
        self.q[state][action_index] = old + self.alpha * (reward + self.gamma * future - old)
    def decay_exploration(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    def greedy_action(self, state):
        return self.choose_action(state, explore=False)
    def export_q_table(self):
        return {"|".join(map(str, state)): values[:] for state, values in self.q.items()}
