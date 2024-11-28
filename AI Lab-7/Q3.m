import numpy as np

class NonStationaryBandit:
    def _init_(self, arms=10):
        self.arms = arms
        self.means = np.zeros(arms)
    
    def step(self):
        self.means += np.random.normal(0, 0.01, self.arms)  
        return self.means

    def reward(self, action):
        return np.random.normal(self.means[action], 1)  

bandit = NonStationaryBandit()
print("Initial Means:", bandit.step())
