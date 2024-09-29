

import heapq

class Node:
    def _init_(self, state, parent=None, g=0, h=0, w1=1, w2=1):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = w1 * g + w2 * h  # Total cost

    def _lt_(self, other):
        return self.f < other.f


def remaining_pegs_heuristic(state):
    # Returns the number of remaining pegs (1s) in the state
    return sum(1 for peg in state if peg == 1)


def get_successors(node):
    """
    Generate valid successors for Marble Solitaire-like moves.
    A valid move consists of a peg jumping over an adjacent peg into an empty space.
    """
    successors = []
    state = list(node.state)

    # Assume 1 = peg, 0 = empty space
    for i in range(len(state) - 2):
        # Peg at i can jump over peg at i+1 into empty spot at i+2 (rightward move)
        if state[i] == 1 and state[i + 1] == 1 and state[i + 2] == 0:
            new_state = state[:]
            new_state[i] = 0
            new_state[i + 1] = 0
            new_state[i + 2] = 1
            successors.append(Node(tuple(new_state), node))

        # Peg at i+2 can jump over peg at i+1 into empty spot at i (leftward move)
        if state[i] == 0 and state[i + 1] == 1 and state[i + 2] == 1:
            new_state = state[:]
            new_state[i] = 1
            new_state[i + 1] = 0
            new_state[i + 2] = 0
            successors.append(Node(tuple(new_state), node))

    return successors


def a_star(start_state, goal_state, heuristic):
    open_list = []
    start_node = Node(start_state, h=heuristic(start_state))
    heapq.heappush(open_list, (start_node.f, start_node))
    visited = set()
    nodes_explored = 0

    while open_list:
        _, node = heapq.heappop(open_list)
        if node.state in visited:
            continue
        visited.add(node.state)
        nodes_explored += 1

        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print('Total nodes explored:', nodes_explored)
            return path[::-1]

        for successor in get_successors(node):
            if successor.state in visited:
                continue
            successor.g = node.g + 1
            successor.h = heuristic(successor.state)
            successor.f = successor.g + successor.h
            heapq.heappush(open_list, (successor.f, successor))

    print('Total nodes explored:', nodes_explored)
    print("No solution found.")
    return None


def best_first_search(start_state, goal_state, heuristic):
    open_list = []
    start_node = Node(start_state, h=heuristic(start_state))
    heapq.heappush(open_list, (start_node.h, start_node))
    visited = set()
    nodes_explored = 0

    while open_list:
        _, node = heapq.heappop(open_list)
        if node.state in visited:
            continue
        visited.add(node.state)
        nodes_explored += 1

        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print('Total nodes explored:', nodes_explored)
            return path[::-1]

        for successor in get_successors(node):
            if successor.state in visited:
                continue
            successor.h = heuristic(successor.state)
            heapq.heappush(open_list, (successor.h, successor))

    print('Total nodes explored:', nodes_explored)
    print("No solution found.")
    return None


# Starting with 31 pegs and an empty space in the center (for Marble Solitaire)
start_state = tuple([1] * 15 + [0] + [1] * 15)
goal_state = tuple([0] * 15 + [1] + [0] * 15)

print("A* Search with Remaining Pegs Heuristic:")
a_star_solution = a_star(start_state, goal_state, remaining_pegs_heuristic)
if a_star_solution:
    print("Solution path found:")
    for step in a_star_solution:
        print(step)
else:
    print("No solution found.")

print("\nBest First Search with Remaining Pegs Heuristic:")
best_first_solution = best_first_search(start_state, goal_state, remaining_pegs_heuristic)
if best_first_solution:
    print("Solution path found:")
    for step in best_first_solution:
        print(step)
else:
    print("No solution found.")