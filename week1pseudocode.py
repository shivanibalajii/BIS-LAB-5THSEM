GENETIC_MODIFICATION:

METHOD initialize():
    population = []
    while population.length == 0:
        wait(10 seconds)
        population.append(random_node())

METHOD select_parents(pop):
    p1 = random_choice(pop)
    p2 = random_choice(pop)
    return p1, p2

METHOD mutate(p1, p2):
    child = crossover(p1, p2)
    for each gene in child:
        if random() < MUTATION_RATE:
            child.gene = random_value()
    return child

METHOD evolve():
    while not done:
        p1, p2 = select_parents(population)
        child = mutate(p1, p2)
        population.add(child)
        population.remove_weakest()
        if best_fitness(population) >= 100:
            done = true
    return population.best()   
