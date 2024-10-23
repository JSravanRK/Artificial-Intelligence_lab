function modified_bandit_agent
    % Parameters
    n_actions = 10;        % Number of bandit arms
    N_steps = 10000;       % Number of steps per experiment
    N_experiments = 10;    % Number of experiments
    eps = 0.1;             % Epsilon for exploration
    alpha = 0.1;           % Step size for non-stationary rewards (EWMA)
    stddev = 0.01;         % Standard deviation for the random walk of probabilities

    % Initialize results storage
    total_rewards = zeros(1, N_steps);  % Reward history over all experiments
    action_counts = zeros(N_steps, n_actions);  % Action selection history
    
    % Run multiple experiments
    for exp = 1:N_experiments
        [actions, rewards] = run_experiment(n_actions, N_steps, eps, alpha, stddev);
        
        % Accumulate rewards and action counts across experiments
        total_rewards = total_rewards + rewards;
        for t = 1:N_steps
            action_counts(t, actions(t)) = action_counts(t, actions(t)) + 1;
        end
        
        % Display progress
        if mod(exp, N_experiments / 10) == 0
            fprintf('[Experiment %d/%d] Average reward: %.4f\n', exp, N_experiments, mean(rewards));
        end
    end

    % Plot results
    plot_results(total_rewards, action_counts, N_experiments, N_steps, n_actions);
end

% Function to simulate the non-stationary environment
function [actions, rewards] = run_experiment(n_actions, N_steps, eps, alpha, stddev)
    % Initialize the environment and agent
    probs = 0.5 * ones(1, n_actions);  % Initial probabilities (mean rewards) for each arm
    Q = zeros(1, n_actions);  % Action-value estimates
    actions = zeros(1, N_steps);  % Store actions
    rewards = zeros(1, N_steps);  % Store rewards

    % Main loop for time steps
    for t = 1:N_steps
        % Epsilon-greedy action selection
        if rand() < eps
            action = randi(n_actions);  % Explore: select a random action
        else
            [~, action] = max(Q);  % Exploit: select the action with the highest Q-value
        end

        % Simulate the environment: pull the arm and get reward
        reward = rand() < probs(action);

        % Update the mean reward probabilities with a random walk
        probs = probs + normrnd(0, stddev, [1, n_actions]);
        probs = max(0, min(probs, 1));  % Ensure probabilities remain between 0 and 1

        % Update Q-value for the chosen action using the exponentially weighted moving average (EWMA)
        Q(action) = Q(action) + alpha * (reward - Q(action));

        % Store the action and reward
        actions(t) = action;
        rewards(t) = reward;
    end
end

% Function to plot the results
function plot_results(total_rewards, action_counts, N_experiments, N_steps, n_actions)
    % Plot the average reward over time
    avg_rewards = total_rewards / N_experiments;
    figure;
    plot(1:N_steps, avg_rewards, '-');
    xlabel('Step');
    ylabel('Average Reward');
    title('Average Reward over Time (EWMA Agent)');
    grid on;
    
    % Plot action selection percentages over time
    figure;
    hold on;
    for action = 1:n_actions
        action_percentage = 100 * action_counts(:, action) / N_experiments;
        plot(1:N_steps, action_percentage, 'LineWidth', 2, 'DisplayName', sprintf('Action %d', action));
    end
    xlabel('Step');
    ylabel('Percentage (%)');
    title('Action Selection Over Time');
    legend('show');
    grid on;
    hold off;
end