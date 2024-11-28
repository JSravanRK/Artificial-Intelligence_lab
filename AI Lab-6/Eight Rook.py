import numpy as np

N = 8 
size = N * N

weights = np.zeros((size, size))

for i in range(N):
    for j in range(N):
        for k in range(i + 1, N): 
            weights[i * N + j, k * N + j] = -2
            weights[k * N + j, i * N + j] = -2
        for k in range(j + 1, N):
            weights[i * N + j, i * N + k] = -2 
            weights[i * N + k, i * N + j] = -2

state = np.random.choice([1, -1], size=size)

def energy(state, weights):
    return -0.5 * np.sum(state * np.dot(weights, state))

def update_state(state, weights):
    for i in range(size):
        net_input = np.dot(weights[i], state)
        state[i] = 1 if net_input > 0 else -1
    return state

iterations = 1000
converged = False

for _ in range(iterations):
    prev_state = state.copy()
    state = update_state(state, weights)
    if np.array_equal(state, prev_state):
        converged = True
        break


if converged:
    print("Solution found:")
else:
    print("Max iterations reached without convergence.")

solution = state.reshape((N, N))
print(solution)