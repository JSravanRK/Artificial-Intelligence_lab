import numpy as np

def binary_bandit(action):
    probabilities = [0.7, 0.5]  # Success probabilities for actions 1 and 2
    return 1 if np.random.rand() < probabilities[action] else 0

def epsilon_greedy_bandit(steps, epsilon=0.1):
    rewards = [0, 0]
    actions = [0, 0]
    total_rewards = 0

    for _ in range(steps):
        if np.random.rand() < epsilon:
            action = np.random.choice([0, 1])  # Explore
        else:
            action = np.argmax(rewards)  # Exploit

        reward = binary_bandit(action)
        total_rewards += reward
        actions[action] += 1
        rewards[action] += (reward - rewards[action]) / actions[action]

    return rewards, total_rewards

results = epsilon_greedy_bandit(10000)
print("Rewards:", results[0])
print("Total Rewards:", results[1])

