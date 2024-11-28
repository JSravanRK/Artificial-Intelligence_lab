import numpy as np

class GbikeMDP:
    def __init__(self):
        self.max_bikes = 20
        self.requests = [3, 4] 
        self.returns = [3, 2]  
        self.discount_factor = 0.9
        
    def transition_probabilities(self, state, action):
       
        new_state = [min(max(state[0] + self.returns[0] - self.requests[0], 0), self.max_bikes),
                      min(max(state[1] + self.returns[1] - self.requests[1], 0), self.max_bikes)]
        
       
        new_state[0] += action
        new_state[1] -= action
        
       
        new_state[0] = max(0, min(new_state[0], self.max_bikes))
        new_state[1] = max(0, min(new_state[1], self.max_bikes))
        
        return tuple(new_state)

    def reward(self, state, action):
        rented_out = min(state[0] + self.returns[0], self.requests[0]) + \
                     min(state[1] + self.returns[1], self.requests[1])
                     
        return rented_out * 10 - abs(action) * 2


gbike_mdp = GbikeMDP()
initial_state = (10, 10)
action = -3 
new_state = gbike_mdp.transition_probabilities(initial_state, action)
reward = gbike_mdp.reward(initial_state, action)

print(f"New State: {new_state}, Reward: {reward}")