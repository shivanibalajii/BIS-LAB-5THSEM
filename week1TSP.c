import random
import math

# Cities with their (x, y) coordinates
cities = {
    0: (0, 0),
    1: (2, 3),
    2: (5, 4),
    3: (6, 1),
    4: (3, 0)
}

POPULATION_SIZE = 10
GENERATIONS = 100
MUTATION_RATE = 0.1


# Calculate distance between two cities
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# Calculate total distance of a route
def fitness(route):
    total = 0

    for i in range(len(route)):
        total += distance(
            route[i],
            route[(i + 1) % len(route)]
        )

    return total


# 1. INITIALIZATION
def initialize_population():
    population = []

    for i in range(POPULATION_SIZE):
        route = list(cities.keys())
        random.shuffle(route)
        population.append(route)

    return population


# 2. EVALUATION
def evaluation(population):
    return sorted(population, key=fitness)


# 3. SELECTION
def selection(population):
    return population[0], population[1]


# 4. CROSSOVER
def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)

    child = [None] * len(parent1)

    child[start:end + 1] = parent1[start:end + 1]

    remaining = [
        city for city in parent2
        if city not in child
    ]

    j = 0

    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1

    return child


# 5. MUTATION
def mutation(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

    return route


# 6. GENETIC ALGORITHM
def genetic_algorithm():
    population = initialize_population()

    for generation in range(GENERATIONS):
        population = evaluation(population)

        new_population = [population[0][:]]

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = selection(population)

            child = crossover(parent1, parent2)

            child = mutation(child)

            new_population.append(child)

        population = new_population

    # Find best solution
    best_route = min(population, key=fitness)

    return best_route, fitness(best_route)


# MAIN PROGRAM
best_route, best_distance = genetic_algorithm()

print("Best Route:", best_route)
print("Shortest Distance:", round(best_distance, 2))
