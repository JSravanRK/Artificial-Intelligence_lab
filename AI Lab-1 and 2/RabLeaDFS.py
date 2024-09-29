initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')

def dfs_rabbit_leap(state, path, visited):
    if state == goal_state:
        return path + [state]

    visited.add(state)
    
    empty_pos = state.index('_')

    for move in [-2, -1, 1, 2]:
        new_pos = empty_pos + move
        if 0 <= new_pos < 7:
            new_state = list(state)
            new_state[empty_pos], new_state[new_pos] = new_state[new_pos], new_state[empty_pos]
            new_state = tuple(new_state)

            if new_state not in visited:
                result = dfs_rabbit_leap(new_state, path + [state], visited)
                if result:
                    return result

    return None

visited = set()
rabbit_solution = dfs_rabbit_leap(initial_state, [], visited)

if rabbit_solution:
    print("Solution found with the following steps:")
    for step in rabbit_solution:
        print(step)
else:
    print("No solution found.")
