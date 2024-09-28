import math
import random
import numpy as np
import matplotlib.pyplot as plt

def read_tsp_file(filename):
    cities = []
    dimension = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('DIMENSION'):
                dimension = int(line.split(':')[1])
            elif line.startswith('NODE_COORD_SECTION'):
                break
        for _ in range(dimension):
            line = f.readline().strip().split()
            cities.append((float(line[1]), float(line[2])))
    return cities

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])*2 + (city1[1] - city2[1])*2)

def tour_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i-1]]) for i in range(len(tour)))

def greedy_initial_solution(cities):
    """ Greedy initial solution based on nearest neighbor heuristic """
    n = len(cities)
    unvisited = list(range(n))
    current_city = random.choice(unvisited)
    solution = [current_city]
    unvisited.remove(current_city)

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: distance(cities[current_city], cities[city]))
        solution.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city

    return solution

def simulated_annealing(cities, initial_temp=1000, cooling_rate=0.999, iterations=100000, min_temp=1e-6):
    n = len(cities)
    current_solution = greedy_initial_solution(cities)  # Use greedy initial solution
    best_solution = current_solution.copy()
    current_length = tour_length(current_solution, cities)
    best_length = current_length
    temp = initial_temp

    for _ in range(iterations):
        if temp <= min_temp:
            break

        # Swap two cities randomly
        new_solution = current_solution.copy()
        i, j = random.sample(range(n), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        new_length = tour_length(new_solution, cities)

        # Metropolis acceptance criterion
        if new_length < current_length or random.random() < math.exp((current_length - new_length) / temp):
            current_solution = new_solution
            current_length = new_length

        if current_length < best_length:
            best_solution = current_solution.copy()
            best_length = current_length

        # Cool down
        temp *= cooling_rate

    return best_solution, best_length

def plot_tour(cities, tour):
    plt.figure(figsize=(10, 10))
    for i in range(len(tour)):
        c1 = cities[tour[i]]
        c2 = cities[tour[i-1]]
        plt.plot([c1[0], c2[0]], [c1[1], c2[1]], 'b-')
    plt.plot([c[0] for c in cities], [c[1] for c in cities], 'ro')
    plt.title("TSP Tour")
    plt.show()

def main():
    filename = 'pka379.tsp'
    cities = read_tsp_file(filename)

    best_tour, best_length = simulated_annealing(cities)

    print(f"Best tour length: {best_length:.2f}")
    plot_tour(cities, best_tour)

if _name_ == "_main_":
    main()
