
import numpy as np
import matplotlib.pyplot as plt
import math

# Generator cost coefficients
a = np.array([500, 400, 200])
b = np.array([5.3, 5.5, 5.8])
c = np.array([0.004, 0.006, 0.009])

Pmin = np.array([50, 50, 50])
Pmax = np.array([200, 150, 100])
Pd = 300

num_nests = 20
max_iter = 100
pa = 0.25

# Fuel cost function
def fitness(P):
    return np.sum(a + b*P + c*P**2)

# Generate feasible solution
def solution():
    P = np.random.uniform(Pmin, Pmax)
    for _ in range(100):
        d = Pd - np.sum(P)
        if abs(d) < 1e-8:
            break
        available = (Pmax-P) if d > 0 else (P-Pmin)
        if np.sum(available) == 0:
            break
        P += np.sign(d) * np.minimum(
            abs(d)*available/np.sum(available), available
        )
    return P

# Initialize nests
nests = np.array([solution() for _ in range(num_nests)])
costs = np.array([fitness(P) for P in nests])

best = nests[np.argmin(costs)].copy()
best_cost = min(costs)
history = []

# Cuckoo Search
for iteration in range(max_iter):

    for i in range(num_nests):

        new = nests[i] + 0.01*np.random.randn(3)*(Pmax-Pmin)
        new = np.clip(new, Pmin, Pmax)

        d = Pd - np.sum(new)
        available = (Pmax-new) if d > 0 else (new-Pmin)

        if np.sum(available) > 0:
            new += np.sign(d)*np.minimum(
                abs(d)*available/np.sum(available), available
            )

        if abs(np.sum(new)-Pd) > 1e-6:
            continue

        j = np.random.randint(num_nests)

        if fitness(new) < costs[j]:
            nests[j] = new
            costs[j] = fitness(new)

    # Abandon worst nests
    order = np.argsort(costs)
    nests = nests[order]
    costs = costs[order]

    for k in range(int((1-pa)*num_nests), num_nests):
        nests[k] = solution()
        costs[k] = fitness(nests[k])

    if min(costs) < best_cost:
        best = nests[np.argmin(costs)].copy()
        best_cost = min(costs)

    history.append(best_cost)

# Display results
print("Optimal Power Generation:")
for i, p in enumerate(best):
    print(f"Generator {i+1}: {p:.2f} MW")

print("Total Generation:", sum(best), "MW")
print("Minimum Fuel Cost:", best_cost)

# Convergence graph
plt.plot(history)
plt.xlabel("Iterations")
plt.ylabel("Minimum Fuel Cost")
plt.title("Cuckoo Search - Economic Load Dispatch")
plt.grid()
plt.show()
