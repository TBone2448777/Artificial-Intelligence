# Most of the code was generated by ChatGPT. The sections written by me are marked accordingly
# Any comments I wrote begin with "Taylor: " if they are not explicitly said to be my code

import random

# Define the coordinates of 20 locations
locations = {
    'A': (0, 0),
    'B': (100, 0),
    'C': (200, 0),
    'D': (300, 0),
    'E': (400, 0),
    'F': (500, 0),
    'G': (500, 100),
    'H': (500, 200),
    'I': (500, 300),
    'J': (500, 400),
    'K': (500, 500),
    'L': (400, 500),
    'M': (300, 500),
    'N': (200, 500),
    'O': (100, 500),
    'P': (0, 500),
    'Q': (0, 400),
    'R': (0, 300),
    'S': (0, 200),
    'T': (0, 100),
}

# Function to calculate the total length of a route
def calculate_total_length(route):
    total_length = 0
    for i in range(len(route) - 1):
        total_length += calculate_distance(route[i], route[i + 1])
    total_length += calculate_distance(route[-1], route[0])  # Return to the starting point
    return total_length

# Function to calculate the Euclidean distance between two locations
def calculate_distance(loc1, loc2):
    x1, y1 = locations[loc1]
    x2, y2 = locations[loc2]
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# Generate an initial population of routes
def generate_population(population_size):
    population = []
    # For however many population size, generate a shuffled order of the location list
    for _ in range(population_size):
        route = list(locations.keys())
        random.shuffle(route)
        population.append(route)
    # Return a list of all the population lists
    return population

# Select parents for crossover using tournament selection
def tournament_selection(population, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament_candidates = random.sample(population, tournament_size)
        winner = min(tournament_candidates, key=lambda x: calculate_total_length(x))
        selected_parents.append(winner)
    return selected_parents

# Perform crossover (ordered crossover)
def ordered_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    for i in range(start, end + 1):
        child[i] = parent1[i]
    remaining = [gene for gene in parent2 if gene not in child]
    child[:start] = [gene for gene in remaining[:start]]
    child[end + 1:] = [gene for gene in remaining[start:]]
    return child

# Perform mutation (swap mutation)
# Taylor: Get a random pice to mutate within a route
def swap_mutation(route):
    mutated_route = route.copy()
    index1, index2 = random.sample(range(len(route)), 2)
    mutated_route[index1], mutated_route[index2] = mutated_route[index2], mutated_route[index1]
    return mutated_route

# This function and comments are my code
# For population go through and add all the total lengths to val. This creates one giant integer for the value of all lists within the generation
# This serves as finding the average length but division would be unnecessary computation so it is just a total sum
def getTotalLength(population):
    val = 0
    for i in population:
        val += calculate_total_length(i)
    return val

# Genetic Algorithm
def genetic_algorithm(population_size, generations, tournament_size, crossover_rate, mutation_rate):
    # Taylor: Gets a random list of however many population_size is. It sets this list of lists equal to population
    population = generate_population(population_size)
    # The below comments and variable definitions are my work
    # These two variables are to tell when to stop. PrevCost is rewritted upon the first find to not be infinite
    # PrevCost tracks if there has been an improvement since the last run, and cycleTime tracks how many generations since no improvement
    prevCost = float('inf')
    cycleTime = 0

    # Max runs is set by the generations variable
    for generation in range(generations):
        # Select parents
        parents = tournament_selection(population, tournament_size)

        # Perform crossover
        # Taylor: Basically take a random index of each parent and swap the left and right halves with one another
        children = []
        for parent1, parent2 in zip(parents[::2], parents[1::2]):
            if random.random() < crossover_rate:
                child1 = ordered_crossover(parent1, parent2)
                child2 = ordered_crossover(parent2, parent1)
                children.extend([child1, child2])
            else:
                children.extend([parent1, parent2])

        # Perform mutation
        # Taylor: Change something randomly within the lists of children
        for i in range(len(children)):
            if random.random() < mutation_rate:
                children[i] = swap_mutation(children[i])

        # Replace old population with new population
        population = children

        # Print the best route and its total length for each generation
        best_route = min(population, key=lambda x: calculate_total_length(x))
        print(f"Generation {generation + 1} - Best Route: {best_route}, Total Length: {calculate_total_length(best_route)}")
        # The below comment and if statement are my code
        # Basically wrote it so that if there is no improvement in 5 times it stops. This leads it to get better answers than just letting it stop after no improvement once
        if prevCost <= getTotalLength(population):
            if cycleTime >= 5:
                break
            cycleTime += 1
        else:
            cycleTime = 0
            prevCost = getTotalLength(population)

    # Return the best route found after all generations
    return min(population, key=lambda x: calculate_total_length(x))

# Set parameters
population_size = 100
generations = 100
tournament_size = 5
crossover_rate = 0.8
mutation_rate = 0.2

# Run the genetic algorithm
best_route = genetic_algorithm(population_size, generations, tournament_size, crossover_rate, mutation_rate)

# Print the final best route and its total length
print("\nFinal Best Route:", best_route)
print("Final Total Length:", calculate_total_length(best_route))