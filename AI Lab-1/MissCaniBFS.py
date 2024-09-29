from collections import deque

initial_state = (3, 3, 0)
goal_state = (0, 0, 1)
moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def is_valid_state(m1, c1, b):
    m2, c2 = 3 - m1, 3 - c1
    return (m1 >= c1 or m1 == 0) and (m2 >= c2 or m2 == 0)

def bfs():
    queue = deque([(initial_state, [])])
    visited = set()
    
    while queue:
        (m1, c1, b), path = queue.popleft()
        
        if (m1, c1, b) == goal_state:
            return path + [(m1, c1, b)]
        
        if (m1, c1, b) in visited:
            continue
        visited.add((m1, c1, b))
        
        for m, c in moves:
            if b == 0:
                new_m1, new_c1 = m1 - m, c1 - c
            else:
                new_m1, new_c1 = m1 + m, c1 + c
            
            if 0 <= new_m1 <= 3 and 0 <= new_c1 <= 3 and is_valid_state(new_m1, new_c1, 1 - b):
                queue.append(((new_m1, new_c1, 1 - b), path + [(m1, c1, b)]))
    
    return None

solution = bfs()

if solution:
    print("Solution found with the following steps:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
