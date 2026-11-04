import random

# Timetable details
subjects = ["Maths", "Physics", "Python", "Civil", "C Programming"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

slots = ["9-10 AM", "10-11 AM", "11-12 PM", "1-2 PM", "2-3 PM"]

SWARM_SIZE = 30
MAX_ITERATIONS = 100

W = 0.5
C1 = 1.5
C2 = 2.5


# Generate a random timetable
def random_position():
    return random.sample(range(25), 5)


# Calculate fitness
def fitness(position):
    penalty = 0

    # Check for duplicate time slots
    if len(set(position)) != len(position):
        penalty += 100

    return penalty


# Particle Swarm Optimization
def pso():

    # Initialization
    swarm = []

    for i in range(SWARM_SIZE):
        position = random_position()
        velocity = [0] * 5

        pbest = position[:]

        swarm.append([position, velocity, pbest])

    gbest = min(swarm, key=lambda x: fitness(x[0]))[0][:]

    # Iterations
    for iteration in range(MAX_ITERATIONS):

        for particle in swarm:

            position = particle[0]
            velocity = particle[1]
            pbest = particle[2]

            # Evaluation
            if fitness(position) < fitness(pbest):
                particle[2] = position[:]

            if fitness(particle[2]) < fitness(gbest):
                gbest = particle[2][:]

            # Update velocity and position
            for j in range(5):

                r1 = random.random()
                r2 = random.random()

                velocity[j] = (
                    W * velocity[j]
                    + C1 * r1 * (pbest[j] - position[j])
                    + C2 * r2 * (gbest[j] - position[j])
                )

                position[j] = round(position[j] + velocity[j])

                # Keep position within valid range
                position[j] = max(0, min(24, position[j]))

    return gbest


# Display timetable
best = pso()

print("\nOPTIMIZED TIME TABLE\n")

for i in range(len(subjects)):

    day = best[i] // 5
    slot = best[i] % 5

    print(subjects[i], "-", days[day], "-", slots[slot])
