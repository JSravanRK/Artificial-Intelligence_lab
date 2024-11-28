import numpy as np

cities = np.array([
    [0, 0], [1, 3], [2, 1], [3, 4], [4, 2], [5, 6], [6, 4], [7, 7], [8, 5], [9, 9]
])

def distance_matrix(cities):
    n = len(cities)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])
    return dist_matrix

dist_matrix = distance_matrix(cities)

N = len(cities)
neurons = N * N
U0 = 0.5  
A, B, C, D = 1500, 1500, 1000, 10

weights = np.zeros((neurons, neurons))
for x in range(N):
    for i in range(N):
        for y in range(N):
            for j in range(N):
                if x == y and i != j:
                    weights[x * N + i, y * N + j] -= A
                elif x != y and i == j:
                    weights[x * N + i, y * N + j] -= B
                elif i == j and x != y:
                    weights[x * N + i, y * N + j] -= C
                else:
                    weights[x * N + i, y * N + j] -= D * dist_matrix[x, y]

def initialize_state_heuristic(N):
    """Generate a heuristic-based valid initial state."""
    state = np.zeros((N, N))
    visited = set()
    for i in range(N):
        for j in range(N):
            if j not in visited:
                state[i, j] = 1
                visited.add(j)
                break
    return state.flatten()

def normalize_state(state, N):
    """Ensure the state satisfies TSP constraints."""
    state = state.reshape((N, N))
    for i in range(N):
        row = state[i, :]
        if np.sum(row) != 1:
            max_idx = np.argmax(row)
            state[i, :] = 0
            state[i, max_idx] = 1
    for j in range(N):
        col = state[:, j]
        if np.sum(col) != 1:
            max_idx = np.argmax(col)
            state[:, j] = 0
            state[max_idx, j] = 1
    return state.flatten()

def update_state(state, weights, U0, N):
    """Update state neurons asynchronously."""
    state = state.flatten()
    for i in range(len(state)):
        net_input = np.dot(weights[i], state) - U0
        state[i] = 1 if net_input > 0 else 0
    return normalize_state(state, N)

def decode_solution(state, N):
    """Decode the TSP route from the state matrix."""
    state = state.reshape((N, N))
    route = []
    for i in range(N):
        if np.sum(state[:, i]) == 1:
            route.append(np.argmax(state[:, i]))
        else:
            return None
    if len(set(route)) == N:
        return route
    return None

def fallback_solution(dist_matrix):
    """Fallback heuristic solution using nearest neighbor."""
    N = len(dist_matrix)
    visited = [0]
    for _ in range(1, N):
        last = visited[-1]
        next_city = np.argmin([dist_matrix[last, j] if j not in visited else np.inf for j in range(N)])
        visited.append(next_city)
    return visited

def run_hopfield_network(dist_matrix, weights, N, neurons, U0, max_attempts=10, iterations=1000):
    for attempt in range(max_attempts):
        state = initialize_state_heuristic(N)
        for _ in range(iterations):
            prev_state = state.copy()
            state = update_state(state, weights, U0, N)
            if np.array_equal(state, prev_state):
                break
        route = decode_solution(state, N)
        if route:
            return route, state
    print("Fallback to heuristic solution.")
    return fallback_solution(dist_matrix), None

route, final_state = run_hopfield_network(dist_matrix, weights, N, neurons, U0)

if route:
    print("Solution found:")
    print("City Visit Sequence:", " → ".join(map(str, route)), "→", route[0])
    total_distance = sum(
        dist_matrix[route[i], route[(i + 1) % N]] for i in range(N)
    )
    print("Total Distance of the route:", total_distance)
else:
    print("Failed to find a valid solution.")