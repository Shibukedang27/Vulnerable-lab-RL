# Q-learning training baseline

Vulnerable-lab-RL includes a dependency-free tabular Q-learning baseline over three fictional security-analysis scenarios and seven predefined structured report actions.

## Train

    python -m vulnerable_lab_rl.train --episodes 12000 --seed 7

The command writes `benchmarks/training_results.json` with the Q-table, learned policy, exploration checkpoints, and evaluation metrics.

## Method

- State: scenario identifier and report phase.
- Action: choose one candidate structured finding report from a finite, synthetic action set.
- Reward: evaluator score normalized to 0..1.
- Policy: epsilon-greedy action selection.
- Update: tabular Q-learning with a learning rate and discount factor.
- Evaluation: greedy policy tested on 100 episodes per scenario after training.

The environment exposes an inspection transition before report submission. The learned choice occurs at the report state; inspection is deterministic and reward-free.

## Results from the committed seed-7 run

- Training episodes: 12,000
- Evaluation episodes: 300 (100 per scenario)
- Mean evaluation reward: 1.0
- Perfect-report rate: 1.0
- Final exploration rate (epsilon): 0.05

These perfect results are expected in this deliberately tiny, finite benchmark: the candidate action set contains the correct synthetic answer for each known scenario. They demonstrate that the implementation learns this finite mapping, not that it generalizes to unseen vulnerabilities or performs real-world penetration testing.

## Next experiments

1. Add held-out scenario templates with different wording and labels.
2. Compare Q-learning against random and rule-based policies.
3. Add multiple valid findings, partial credit, and evidence-quality checks.
4. Consider a neural policy only after the state/action space justifies it.
