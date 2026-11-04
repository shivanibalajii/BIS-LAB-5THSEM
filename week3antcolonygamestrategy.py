import random

# Game paths and their costs
game_paths = {
    0: [(1, 2), (2, 4)],
    1: [(2, 2), (3, 3)],
    2: [(1, 5), (3, 1)],
    3: [(2, 3), (3, 2)]
}

# Parameters
NUM_ANTS = 10
MAX_ITERATIONS = 50

ALPHA = 1
BETA = 2
EVAPORATION = 0.5
Q = 100

# Initialize pheromones
pheromone = {
    path: 1.0 for path in game_paths
}


# Calculate total cost of a strategy
def calculate_cost(path):
    return sum(cost for action, cost in game_paths[path])


# Calculate probability of selecting a path
def probability(path, available_paths):
    total = 0

    for p in available_paths:
        total += (
            pheromone[p] ** ALPHA
            * (1 / calculate_cost(p)) ** BETA
        )

    return (
        pheromone[path] ** ALPHA
        * (1 / calculate_cost(path)) ** BETA
    ) / total


# Select a game strategy
def select_path(available_paths):
    probabilities = [
        probability(p, available_paths)
        for p in available_paths
    ]

    return random.choices(
        available_paths,
        weights=probabilities
    )[0]


# Ant Colony Optimization
def aco():
    best_path = None
    best_cost = float('inf')

    for iteration in range(MAX_ITERATIONS):
        all_paths = []

        # Each ant selects a strategy
        for ant in range(NUM_ANTS):
            available_paths = list(game_paths.keys())

            selected_path = select_path(available_paths)

            cost = calculate_cost(selected_path)

            all_paths.append((selected_path, cost))

            if cost < best_cost:
                best_cost = cost
                best_path = selected_path

        # Evaporate old pheromones
        for path in pheromone:
            pheromone[path] *= (1 - EVAPORATION)

        # Deposit new pheromones
        for path, cost in all_paths:
            pheromone[path] += Q / cost

    return best_path, best_cost


# Main program
best_path, best_cost = aco()

print("BEST GAME STRATEGY")
print("Selected Path:", best_path)
print("Actions:", game_paths[best_path])
print("Minimum Cost:", best_cost)
