import numpy as np

class GbikeMDP:
    def __init__(self):
        self.max_bikes = 20
        self.requests = [3, 4] 
        self.returns = [3, 2]    
        self.discount_factor = 0.9
        self.additional_parking_cost = 4
        self.parking_threshold = 10

    def transition_probabilities(self, state, action):
        bikes_at_loc1, bikes_at_loc2 = state
        if action > 0: 
            if action == 1: 
                bikes_at_loc1 -= 1
                bikes_at_loc2 += 1
                action -= 1  
            else:
                bikes_at_loc1 -= action
                bikes_at_loc2 += action

        elif action < 0: 
            bikes_at_loc1 -= action 
            bikes_at_loc2 += -action
        
       
        new_bikes_at_loc1 = min(max(bikes_at_loc1 + self.returns[0] - self.requests[0], 0), self.max_bikes)
        new_bikes_at_loc2 = min(max(bikes_at_loc2 + self.returns[1] - self.requests[1], 0), self.max_bikes)

        return (new_bikes_at_loc1, new_bikes_at_loc2)

    def parking_cost(self, state):
        cost = 0
        if state[0] > self.parking_threshold:
            cost += self.additional_parking_cost
        if state[1] > self.parking_threshold:
            cost += self.additional_parking_cost
        return cost

    def reward(self, state, action):
        rented_out = min(state[0] + self.returns[0], self.requests[0]) + \
                     min(state[1] + self.returns[1], self.requests[1])
        
        move_cost = max(0, (abs(action) - 1) * 2)  
        
        return rented_out * 10 - move_cost - self.parking_cost(state)

    def policy_iteration(self):
        states = [(x1, x2) for x1 in range(self.max_bikes + 1) for x2 in range(self.max_bikes + 1)]
        policy = {state: 0 for state in states}  
        value_function = {state: 0 for state in states}
        theta = 1e-6

        while True:
           
            while True:
                delta = 0
                for state in states:
                    v = value_function[state]
                    action = policy[state]
                    new_state = self.transition_probabilities(state, action)
                    value_function[state] = self.reward(state, action) + \
                        self.discount_factor * value_function[new_state]
                    delta = max(delta, abs(v - value_function[state]))
                if delta < theta:
                    break

           
            policy_stable = True
            for state in states:
                old_action = policy[state]
               
                action_values = []
                for action in range(-5, 6):
                    new_state = self.transition_probabilities(state, action)
                    action_value = self.reward(state, action) + \
                        self.discount_factor * value_function[new_state]
                    action_values.append(action_value)
                
                best_action = np.argmax(action_values) - 5
                policy[state] = best_action
                
                if old_action != policy[state]:
                    policy_stable = False

            if policy_stable:
                break

        return policy, value_function
gbike_mdp = GbikeMDP()
policy, value_function = gbike_mdp.policy_iteration()

print("Final Policy:", policy)
print("Final Value Function:", value_function)