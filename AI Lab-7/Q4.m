def epsilon_greedy_nonstationary(steps, epsilon=0.1):
    bandit = NonStationaryBandit()
    rewards = np.zeros(bandit.arms)
    actions = np.zeros(bandit.arms)
    total_rewards = 0

    for t in range(steps):
        if np.random.rand() < epsilon:
            action = np.random.choice(bandit.arms)  # Explore
        else:
            action = np.argmax(rewards)  # Exploit

        reward = bandit.reward(action)
        total_rewards += reward
        actions[action] += 1
        rewards[action] += (reward - rewards[action]) / actions[action]  # Update

        # Update bandit means
        bandit.step()

    return rewards, total_rewards

results = epsilon_greedy_nonstationary(10000)
print("Rewards:", results[0])
print("Total Rewards:", results[1])
