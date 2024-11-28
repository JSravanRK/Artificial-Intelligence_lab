import numpy as np

patterns = np.array([
    np.random.choice([1, -1], size=(10, 10)) for _ in range(5)
])

patterns_1d = [p.flatten() for p in patterns]
weights = np.zeros((100, 100))

for p in patterns_1d:
    weights += np.outer(p, p)

np.fill_diagonal(weights, 0)

def update_state(state, weights):
    for i in range(len(state)):
        net_input = np.dot(weights[i], state)
        state[i] = 1 if net_input > 0 else -1
    return state

input_pattern = patterns_1d[0] + np.random.choice([1, -1], size=100) * 0.3
input_pattern = np.sign(input_pattern)

state = input_pattern
for _ in range(10):
    state = update_state(state, weights)

state_2d = state.reshape((10, 10))
print("Recovered Pattern:")
print(state_2d)

N = 100
capacity = 0.15 * N
print(f"Maximum capacity of the Hopfield network: {capacity}")

def test_error_correction(patterns_1d, weights):
    noisy_input = patterns_1d[0] + np.random.choice([1, -1], size=100) * 0.3
    noisy_input = np.sign(noisy_input)

    state = noisy_input
    for _ in range(10):
        state = update_state(state, weights)

    return state

corrected_pattern = test_error_correction(patterns_1d, weights)
corrected_pattern_2d = corrected_pattern.reshape((10, 10))
print("Corrected Pattern:")
print(corrected_pattern_2d)