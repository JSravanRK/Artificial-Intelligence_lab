moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
initial_state = (3, 3, 0)
goal_state = (0, 0, 1)

def is_valid_state(m1, c1, b):
    m2, c2 = 3 - m1, 3 - c1
    return (m1 >= c1 or m1 == 0) and (m2 >= c2 or m2 == 0)

def dfs(state, path, visited):
    m1, c1, b = state
    if state == goal_state:
        return path + [state]
    
    visited.add(state)
    
    for m, c in moves:
        if b == 0:
            new_m1, new_c1 = m1 - m, c1 - c
        else:
            new_m1, new_c1 = m1 + m, c1 + c
        
        new_state = (new_m1, new_c1, 1 - b)
        if 0 <= new_m1 <= 3 and 0 <= new_c1 <= 3 and is_valid_state(new_m1, new_c1, 1 - b) and new_state not in visited:
            result = dfs(new_state, path + [state], visited)
            if result:
                return result
    
    return None

solution = dfs(initial_state, [], set())

if solution:
    print("Solution found with the following steps:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
