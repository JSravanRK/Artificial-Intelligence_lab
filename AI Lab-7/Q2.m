function [total_rewards, action_history] = modified_epsilon_greedy_bandit(time_steps)
    % Initialize parameters
    k = 10; % Number of arms
    epsilon = 0.1; % Exploration rate
    alpha = 0.1; % Step-size parameter (for non-stationary environment)
    
    q_true = zeros(1, k); % True action values
    q_est =% Initialize parameters
bandit_probs = [0.4, 0.6];  % Success probabilities for binaryBanditA and binaryBanditB
N_steps = 1000;  % Number of episodes
eps = 0.1;  % Epsilon for exploration
nActions = length(bandit_probs);  % Number of actions (binaryBanditA, binaryBanditB)

% Initialize agent parameters
Q = zeros(1, nActions);  % Action-value estimates
n = zeros(1, nActions);  % Number of times each action has been taken
actions = zeros(1, N_steps);  % Store actions
rewards = zeros(1, N_steps);  % Store rewards

% Function to simulate binary bandit
binaryBandit = @(p) rand() < p;  % Returns 1 with probability p, otherwise 0

% Run epsilon-greedy experiment
for step = 1:N_steps
    % Epsilon-greedy action selection
    if rand() < eps
        action = randi(nActions);  % Explore: choose random action
    else
        [~, action] = max(Q);  % Exploit: choose action with highest Q-value
    end

    % Get reward from the selected bandit
    reward = binaryBandit(bandit_probs(action));

    % Update the count for the selected action
    n(action) = n(action) + 1;

    % Update Q-value estimate using incremental mean formula
    Q(action) = Q(action) + (1 / n(action)) * (reward - Q(action));

    % Store action and reward
    actions(step) = action;
    rewards(step) = reward;
end

% Plot the average reward over time
avg_reward = cumsum(rewards) ./ (1:N_steps);
figure;
plot(1:N_steps, avg_reward);
xlabel('Step');
ylabel('Average Reward');
title(['Epsilon-Greedy: Epsilon = ', num2str(eps)]);
grid on;

% Plot histogram of action selection
figure;
histogram(actions, 'BinEdges', 0.5:1:nActions+0.5, 'Normalization', 'count');
xlabel('Action (1 = Bandit A, 2 = Bandit B)');
ylabel('Count');
title('Action Selection Histogram');
grid on; zeros(1, k);  % Estimated action values
    total_rewards = zeros(1, time_steps); % Store rewards over time
    action_history = zeros(1, time_steps); % Store action history

    for t = 1:time_steps
        % Update the true action values (random walk)
        q_true = q_true + normrnd(0, 0.01, 1, k);
        
        % Epsilon-greedy action selection
        if rand < epsilon
            % Exploration: Choose a random action
            action = randi(k);
        else
            % Exploitation: Choose the action with the highest estimated reward
            [~, action] = max(q_est);
        end
        
        % Reward received from the chosen action (random around true mean)
        reward = normrnd(q_true(action), 1);
        
        % Update the estimated value using the step-size parameter (α)
        q_est(action) = q_est(action) + alpha * (reward - q_est(action));
        
        % Store the reward and action taken
        total_rewards(t) = reward;
        action_history(t) = action;
    end
end