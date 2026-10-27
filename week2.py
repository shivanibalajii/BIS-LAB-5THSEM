def get_cost(sched):
    # Calculates total tardiness cost of the schedule
    time, cost = 0, 0
    for dur, dl in sched:
        time += dur
        cost += max(0, time - dl)
    return cost

def schedule_task(existing, new_task):
    # Evaluates every position to insert the new task and returns the best schedule
    best_sched, min_cost = None, float('inf')
    for i in range(len(existing) + 1):
        candidate = existing[:i] + [new_task] + existing[i:]
        cost = get_cost(candidate)
        print(f"Position {i}: {candidate} -> Cost: {cost}")
        if cost < min_cost:
            min_cost, best_sched = cost, candidate
    return best_sched

# Representation: (duration, deadline) 
existing_schedule = [(3, 4), (2, 5)]
new_task = (4, 6)

print(f"Initial Schedule: {existing_schedule}")
optimal = schedule_task(existing_schedule, new_task)
print(f"\nOptimal Schedule: {optimal}")
