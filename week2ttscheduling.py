
import random

# Timetable details
subjects = ["Maths", "Physics", "Python", "Civil", "C Programming"]

sections = ["A", "B", "C"]

classrooms = [
    "Room 1", "Room 2", "Room 3", "Room 4",
    "Room 5", "Room 6", "Room 7", "Room 8"
]

day = "Monday"

SWARM_SIZE = 30
MAX_ITERATIONS = 100

W = 0.5
C1 = 1.5
C2 = 2.5


# Generate random classroom assignments
def random_position():
    return [
        random.randint(0, 7)
        for i in range(15)
    ]


# Calculate fitness
def fitness(position):
    penalty = 0

    # Check classroom clashes between sections
    for i in range(5):
        assigned_rooms = [
            position[i],
            position[i + 5],
            position[i + 10]
        ]

        if len(set(assigned_rooms)) != 3:
            penalty += 100

    return penalty


# Particle Swarm Optimization
def pso():

    swarm = []

    # Initialization
    for i in range(SWARM_SIZE):
        position = random_position()
        velocity = [0.0] * 15
        pbest = position[:]

        swarm.append([position, velocity, pbest])

    gbest = min(
        swarm,
        key=lambda x: fitness(x[0])
    )[0][:]

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
            for j in range(15):

                r1 = random.random()
                r2 = random.random()

                velocity[j] = (
                    W * velocity[j]
                    + C1 * r1 * (pbest[j] - position[j])
                    + C2 * r2 * (gbest[j] - position[j])
                )

                position[j] = round(
                    position[j] + velocity[j]
                )

                position[j] = max(
                    0, min(7, position[j])
                )

    return gbest


# Main program
best = pso()

print("\nOPTIMIZED TIMETABLE\n")

# Display timetable
for s in range(3):

    print("\nSection:", sections[s])

    for i in range(5):

        room = best[s * 5 + i]

        print(
            day, "-",
            subjects[i], "-",
            classrooms[room]
        )
