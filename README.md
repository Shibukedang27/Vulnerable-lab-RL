# Vulnerable-lab-RL

**Reinforcement-learning-style environments for evaluating AI security analysis.**

Vulnerable-lab-RL is a local, deterministic benchmark built around fictional application-security scenarios. An agent receives a scenario, inspects its description, submits a structured finding, and receives a score based on a transparent rubric.

> **Safety boundary:** This project is an evaluation sandbox, not an exploit toolkit. It does not scan networks, connect to external targets, execute payloads, or exploit real software. All scenarios are synthetic.

## What it evaluates

- Recognition of common security design weaknesses
- Correct classification of finding severity
- Evidence-based explanations
- Repeatable agent performance across scenarios

## Quick start

Requires Python 3.10+ and has no third-party runtime dependencies.

```bash
python -m vulnerable_lab_rl.cli list
python -m vulnerable_lab_rl.cli demo
python -m unittest discover -s tests -v
```

## Environment interaction

The environment exposes a small episode interface:

1. `reset(scenario_id)` returns the scenario observation.
2. `step(action)` accepts `inspect`, `submit`, or `finish`.
3. The episode ends after submission or finish and returns a rubric score.

Example action:

```python
{
    "type": "submit",
    "finding_id": "AUTHZ-MISSING-OWNERSHIP-CHECK",
    "severity": "high",
    "evidence": "The design does not verify that the authenticated user owns the requested record."
}
```

See `examples/run_episode.py` for a complete walkthrough.

## Project structure

```text
Vulnerable-lab-RL/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/vulnerable_lab_rl/
│   ├── __init__.py
│   ├── scenarios.py
│   ├── environment.py
│   ├── evaluator.py
│   └── cli.py
├── examples/
│   └── run_episode.py
└── tests/
    ├── test_environment.py
    └── test_evaluator.py
```

## Current limitations

- The scenarios and answer keys are intentionally small and synthetic.
- The current baseline is a deterministic episodic environment; it does not train a reinforcement-learning policy.
- Evidence scoring checks presence and minimum length, not semantic correctness.
- Results should be treated as benchmark signals, not proof of real-world security expertise.

## Roadmap

- Expand the synthetic scenario set and version the scoring rubric.
- Add episode traces and aggregate benchmark reports.
- Add an optional Gymnasium adapter.
- Compare agent policies across fixed scenario seeds.

## Responsible use

Use this project for local education and authorized evaluation only. Do not test systems without explicit permission.

## License

MIT. See [LICENSE](LICENSE).

## Reinforcement-learning baseline

A dependency-free tabular Q-learning agent and reproducible training runner are included. Train with:

```bash
python -m vulnerable_lab_rl.train --episodes 12000 --seed 7
```

See [docs/TRAINING.md](docs/TRAINING.md) for the algorithm, evaluation protocol, limitations, and committed [training artifact](benchmarks/training_results.json). The initial benchmark is deliberately finite and synthetic; its perfect score demonstrates learning the small candidate mapping, not generalization to unseen vulnerabilities or real-world penetration-testing capability.
