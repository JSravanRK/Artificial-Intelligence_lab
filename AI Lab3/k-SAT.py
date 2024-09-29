
import random
import time

def generate_k_sat_problem(k, m, n):
    """generates a random k-SAT problem with given parameters.
    """

    problem = []
    variables = [f"x{i}" for i in range(1, n + 1)]

    for _ in range(m):
        clause = []
        selected_vars = random.sample(variables, k)
        for var in selected_vars:
            literal = var if random.choice([True, False]) else f"~{var}"
            clause.append(literal)
        problem.append(clause)

    return problem

def evaluate_clause(clause, assignment):
    """Evaluates a clause given an assignment."""

    return any((literal[1:] if literal.startswith('~') else literal) in assignment for literal in clause)

def hill_climbing(problem, n):
    """Solves a k-SAT problem using the hill climbing algorithm. """

    current_assignment = random.sample([f"x{i}" for i in range(1, n + 1)], n)
    steps = 0

    while True:
        satisfied_clauses = sum(evaluate_clause(clause, current_assignment) for clause in problem)

        if satisfied_clauses == len(problem):
            return current_assignment, steps

        next_assignment = current_assignment[:]
        random.shuffle(next_assignment)
        steps += 1

        if sum(evaluate_clause(clause, next_assignment) for clause in problem) > satisfied_clauses:
            current_assignment = next_assignment

def beam_search(problem, n, beam_width=3):
    """Solves a k-SAT problem using the beam search algorithm."""

    beams = [random.sample([f"x{i}" for i in range(1, n + 1)], n) for _ in range(beam_width)]
    steps = 0

    while True:
        best_assignment = max(beams, key=lambda assignment: sum(evaluate_clause(clause, assignment) for clause in problem))

        if sum(evaluate_clause(clause, best_assignment) for clause in problem) == len(problem):
            return best_assignment, steps

        new_beams = []
        for _ in range(beam_width):
            new_assignment = best_assignment[:]
            random.shuffle(new_assignment)
            new_beams.append(new_assignment)
        beams = new_beams
        steps += 1

def vnd(problem, n):
    """Solves a k-SAT problem using the variable neighborhood descent algorithm."""

    current_assignment = random.sample([f"x{i}" for i in range(1, n + 1)], n)
    neighborhood_functions = [
        lambda x: x[::-1],  #Simple reversal
        lambda x: sorted(x),
        lambda x: random.sample(x, len(x))  # Random shuffle
    ]

    steps = 0

    for neighborhood in neighborhood_functions:
        next_assignment = neighborhood(current_assignment)
        if sum(evaluate_clause(clause, next_assignment) for clause in problem) > sum(evaluate_clause(clause, current_assignment) for clause in problem):
            current_assignment = next_assignment
            break
        steps += 1

    return current_assignment, steps

# Example of generating a random 3-SAT problem and solving it
k = 3
m = 10
n = 5

sat_problem = generate_k_sat_problem(k, m, n)

print("\nHill Climbing Solution:")
start_time = time.time()
hill_solution = hill_climbing(sat_problem, n)
end_time = time.time()
print(f"Assignment: {hill_solution[0]}, Steps: {hill_solution[1]}, Time: {end_time - start_time:.5f} seconds")

print("\nBeam Search Solution:")
start_time = time.time()
beam_solution = beam_search(sat_problem, n, beam_width=3)
end_time = time.time()
print(f"Assignment: {beam_solution[0]}, Steps: {beam_solution[1]}, Time: {end_time - start_time:.5f} seconds")

print("\nVariable Neighborhood Descent Solution:")
start_time = time.time()
vnd_solution = vnd(sat_problem, n)
end_time = time.time()
print(f"Assignment: {vnd_solution[0]}, Steps: {vnd_solution[1]}, Time: {end_time - start_time:.5f} seconds")