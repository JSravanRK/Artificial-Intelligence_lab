import numpy as np

class GridWorld:
    def __init__(self, reward):
        self.grid_size = (4, 3)
        self.actions = ['Up', 'Down', 'Left', 'Right']
        self.reward = reward
        self.terminal_states = {(0, 2): 1, (1, 2): -1}
        self.gamma = 0.9 
        self.value_function = np.zeros(self.grid_size)

    def is_terminal(self, state):
        return state in self.terminal_states

    def get_reward(self, state):
        if state in self.terminal_states:
            return self.terminal_states[state]
        return self.reward

    def transition(self, state, action):
        row, col = state
        
        if action == 'Up':
            next_state = (max(row - 1, 0), col)
        elif action == 'Down':
            next_state = (min(row + 1, self.grid_size[0] - 1), col)
        elif action == 'Left':
            next_state = (row, max(col - 1, 0))
        elif action == 'Right':
            next_state = (row, min(col + 1, self.grid_size[1] - 1))

        return next_state

    def value_iteration(self):
        while True:
            delta = 0
            new_value_function = np.copy(self.value_function)

            for row in range(self.grid_size[0]):
                for col in range(self.grid_size[1]):
                    state = (row, col)

                    if self.is_terminal(state):
                        continue
                    
                    action_values = []
                    
                    for action in self.actions:
                        intended_state = self.transition(state, action)
                        
                       
                        expected_value = (
                            0.8 * new_value_function[intended_state] +
                            0.1 * new_value_function[self.transition(state, 'Left')] +
                            0.1 * new_value_function[self.transition(state, 'Right')]
                        )
                        
                        action_values.append(expected_value)

                    new_value_function[state] = self.get_reward(state) + self.gamma * max(action_values)
                    delta = max(delta, abs(new_value_function[state] - self.value_function[state]))

            self.value_function = new_value_function
            
            if delta < 1e-6:  
                break

        return self.value_function

reward_settings = [-2, 0.1, 0.02, 1]

for r in reward_settings:
    grid_world = GridWorld(reward=r)
    value_function = grid_world.value_iteration()
    print(f"Value Function for r(s)={r}:\n{value_function}\n")