"""Command-line tools for Vulnerable-lab-RL."""

import argparse
import json

from .environment import SecurityEvaluationEnv
from .scenarios import SCENARIOS


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic AI security evaluation environment")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list available synthetic scenarios")
    sub.add_parser("demo", help="run a perfect-match demonstration episode")
    args = parser.parse_args()

    if args.command == "list":
        print(json.dumps([
            {"scenario_id": key, "title": value["title"]}
            for key, value in SCENARIOS.items()
        ], indent=2))
        return

    env = SecurityEvaluationEnv()
    observation = env.reset("AUTHZ-001")
    expected = SCENARIOS["AUTHZ-001"]["expected"]
    print("Observation:")
    print(json.dumps(observation, indent=2))
    _, reward, done, info = env.step({
        "type": "submit",
        **expected,
        "evidence": "The design does not verify that the authenticated user owns the requested record.",
    })
    print("\nEpisode result:")
    print(json.dumps({"reward": reward, "done": done, "metrics": info}, indent=2))


if __name__ == "__main__":
    main()
