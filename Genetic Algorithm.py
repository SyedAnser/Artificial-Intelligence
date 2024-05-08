import numpy as np
import matplotlib.pyplot as plt

# Define the fitness function
def fitness_function(x):
    return 1 - (x**2)

# Decode binary representation to real number
def decode_chromosome(chromosome):
    x_min, x_max = -5, 5
    x_range = x_max - x_min
    return x_min + int(chromosome, 2) * (x_range / (2**len(chromosome) - 1))

# Initialize population
def initialize_population(pop_size, chrom_length): #To make a population
    choice = ['0','1']
    arr = []
    for i in range(pop_size):
        str = ''
        for j in range(chrom_length):
            str += np.random.choice(choice)
        arr.append(str)  
    return arr

# Roulette wheel selection
def select_parents(population, fitness):
    total_fitness = np.sum(fitness)
    probabilities = fitness / total_fitness
    return np.random.choice(len(population), size=2, p=probabilities)


# Single-point crossover
def crossover(parent1, parent2):
    crossover_point = np.random.randint(1, len(parent1))
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutation (single bit flip)
def mutate(chromosome, mutation_prob):
    chromosome_list = list(chromosome)
    mutation_point = np.random.randint(0, len(chromosome))
    if np.random.rand() < mutation_prob:
        if chromosome_list[mutation_point] == '0':
            chromosome_list[mutation_point] = '1'
        else:
            chromosome_list[mutation_point] = '0'
    return ''.join(chromosome_list)

# Main Genetic Algorithm function
def genetic_algorithm(pop_size, chrom_length, generations):
    population = initialize_population(pop_size, chrom_length)
    print("Initial population:",population)
    best_fitness = []
    avg_fitness = []

    for gen in range(generations):
        # Decode chromosomes and calculate fitness
        decoded_population = np.array([decode_chromosome(chrom) for chrom in population], dtype=float)
        fitness = (fitness_function(decoded_population))
        fitness -= np.min(fitness)

       # Record best and average fitness
        best_fitness.append(np.max(fitness))
        avg_fitness.append(np.mean(fitness))

        # Selection
        parents_indices = select_parents(population, fitness)
        parent1, parent2 = population[parents_indices[0]], population[parents_indices[1]]

        # Crossover
        child1, child2 = crossover(parent1, parent2)

        # Mutation
        child1 = mutate(child1, mutation_prob=0.01)
        child2 = mutate(child2, mutation_prob=0.01)

        # Replace parents with offspring
        population[parents_indices[0]], population[parents_indices[1]] = child1, child2

    return best_fitness, avg_fitness, population

# Run GA
pop_size = 10
chrom_length = 10
generations = 100

best_fitness, avg_fitness, population = genetic_algorithm(pop_size, chrom_length, generations)

# Plotting
plt.plot(range(generations), best_fitness, label='Best Fitness')
plt.plot(range(generations), avg_fitness, label='Average Fitness')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()
plt.title('Genetic Algorithm: Maximize f(x) = 1 - x^2')
plt.show()

# Print final result
decoded_population = np.array([decode_chromosome(chrom) for chrom in population], dtype=float)
print("Final population:",population)
print("decoded:", decoded_population)
best_solution_index = np.argmax((fitness_function(decoded_population)))
best_solution = decoded_population[best_solution_index]
print("Final value of x that maximizes f(x):", best_solution)
print("Maximum fitness (f(x)):", fitness_function(best_solution))
