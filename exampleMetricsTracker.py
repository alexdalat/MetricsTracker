import sys
import random
from MetricTracker import MetricTracker

def run_session():
    # Initialize the MetricTracker with metrics of interest
    mt = MetricTracker(['episode_num', 'reward'])

    current_reward = 50

    for episode in range(1, 11):
        step = random.choice([-10, -5, 0, 5, 10])  # Random step to simulate variability in reward
        current_reward += step
        mt.log_metrics(episode, current_reward)
        print(f"Logged Episode {episode}, Reward {current_reward}")

    # Plot the current metrics
    mt.plot_current_metrics()

    # Plot the comparison with the previous session's data if available
    mt.plot_comparison()

if __name__ == '__main__':
    run_session()

