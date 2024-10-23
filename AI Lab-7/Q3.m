function [total_rewards, action_history] = modified_epsilon_greedy_bandit(time_steps)
    % Initialize parameters
    k = 10; % Number of arms
    epsilon = 0.1; % Exploration rate
    alpha = 0.1; % Step-size parameter (for non-stationary environment)
    
    q_true = zeros(1, k); % True action values
    q_est = zeros(1, k);  % Estimated action values
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