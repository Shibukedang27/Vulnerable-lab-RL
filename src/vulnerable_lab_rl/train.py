"""Train and evaluate a tabular Q-learning agent on fictional scenarios."""
import argparse, json, random
from pathlib import Path
from .environment import SecurityEvaluationEnv
from .rl_agent import CANDIDATES, QLearningAgent
from .scenarios import SCENARIOS

def run_episode(agent, env, scenario_id, explore=True):
    env.reset(scenario_id)
    env.step({"type": "inspect"})
    state = (scenario_id, "report")
    action_index = agent.choose_action(state, explore=explore)
    _, reward, done, metrics = env.step(CANDIDATES[action_index].as_dict())
    if explore:
        agent.update(state, action_index, reward, None, done)
    return reward, metrics.get("score", 0) == 100

def evaluate(agent, episodes_per_scenario=100):
    env, rewards, perfect = SecurityEvaluationEnv(), [], 0
    for scenario_id in SCENARIOS:
        for _ in range(episodes_per_scenario):
            reward, is_perfect = run_episode(agent, env, scenario_id, explore=False)
            rewards.append(reward)
            perfect += int(is_perfect)
    total = len(rewards)
    return {"episodes": total, "mean_reward": round(sum(rewards) / max(1, total), 4), "perfect_report_rate": round(perfect / max(1, total), 4)}

def random_baseline(episodes_per_scenario=100, seed=7):
    """Evaluate uniformly random candidate reports as a simple baseline."""
    rng, env, rewards, perfect = random.Random(seed), SecurityEvaluationEnv(), [], 0
    for scenario_id in SCENARIOS:
        for _ in range(episodes_per_scenario):
            env.reset(scenario_id)
            env.step({"type": "inspect"})
            action = CANDIDATES[rng.randrange(len(CANDIDATES))].as_dict()
            _, reward, _, metrics = env.step(action)
            rewards.append(reward)
            perfect += int(metrics.get("score", 0) == 100)
    total = len(rewards)
    return {"episodes": total, "mean_reward": round(sum(rewards) / total, 4), "perfect_report_rate": round(perfect / total, 4)}


def train(episodes=12000, seed=7):
    rng, agent, env = random.Random(seed), QLearningAgent(seed=seed), SecurityEvaluationEnv()
    scenario_ids, checkpoints = list(SCENARIOS), []
    for episode in range(1, episodes + 1):
        run_episode(agent, env, rng.choice(scenario_ids), explore=True)
        agent.decay_exploration()
        if episode % max(1, episodes // 20) == 0:
            checkpoints.append({"episode": episode, "epsilon": round(agent.epsilon, 5)})
    metrics = evaluate(agent)
    metrics["random_baseline"] = random_baseline(seed=seed)
    metrics.update({"training_episodes": episodes, "seed": seed, "final_epsilon": round(agent.epsilon, 5), "learning_checkpoints": checkpoints})
    return agent, metrics

def main():
    parser = argparse.ArgumentParser(description="Train the synthetic VulnLab-RL Q-learning baseline")
    parser.add_argument("--episodes", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/training_results.json"))
    args = parser.parse_args()
    if args.episodes < 1:
        parser.error("--episodes must be positive")
    agent, metrics = train(args.episodes, args.seed)
    payload = {"algorithm": "tabular Q-learning", "action_space_size": len(CANDIDATES), "scenarios": list(SCENARIOS), "metrics": metrics, "q_table": agent.export_q_table(), "learned_policy": {sid: CANDIDATES[agent.greedy_action((sid, "report"))].as_dict() for sid in SCENARIOS}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "q_table"}, indent=2))
    print(f"\nSaved full training artifact to {args.output}")

if __name__ == "__main__":
    main()
