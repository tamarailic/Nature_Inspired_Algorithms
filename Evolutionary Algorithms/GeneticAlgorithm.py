import random

def one_max(bitstring):
    sumation = 0
    for bit in bitstring:
        if bit == "1":
            sumation += 1
    return sumation * (-1)

def random_bitstring():
    bitstring = ''
    for i in range(num_bits):
        random_chance = random.random()
        if random_chance >= 0.5:
            bitstring += '1'
        else:
            bitstring += '0'

    return bitstring

def tournaments_selection(population):
    parents = []
    for _ in range(len(population)):
        parents.append(population[binary_tournament(population)])
  
    return parents

def binary_tournament(population):
    random_opponent1 = random.randint(0,len(population) - 1)
    random_opponent2 = random.randint(0,len(population) - 1)
    while random_opponent1 == random_opponent2: 
        random_opponent2 = random.randint(0,len(population) - 1)
    
    if one_max(population[random_opponent1]) <= one_max(population[random_opponent2]):
        return random_opponent1
    return random_opponent2

def crossover_bitstring(parents):
    if random.random() >= crossover_rate:
        return parents[0], parents[1]
    bound = random.randint(0, len(parents[0])-1)
    child1 = parents[0][:bound] + parents[1][bound:]
    child2 = parents[1][:bound] + parents[0][bound:]

    return child1, child2

def mutate_bitstring(bitstring):
    for i in range(len(bitstring)):
        random_chance = random.random()
        if random_chance <= mutation_rate:
            if bitstring[i] == '1':
                bitstring.replace(bitstring[i],'0')
            else:
                bitstring.replace(bitstring[i],'1')
    return bitstring

def replace_population(population, children):
    return children

def bitstring_stop(best):
    global iteration_num
    iteration_num -= 1
    return one_max(best) == -1 * num_bits or iteration_num <= 0

#problem domain functions
cost_function = one_max
generate_genom_function = random_bitstring
select_best_parents_function = tournaments_selection
crossover_domain_function = crossover_bitstring
mutation_domain_function = mutate_bitstring
domain_replace_population_function = replace_population
stop_condition = bitstring_stop

def genetic_alghorithm():
    population = initialize_population()
    evaluate_population(population)
    return search_for_best_solution(population)

def initialize_population():
    #make random population based on problem given
    population = []
    for i in range(population_num):
        genom = generate_genom_function()
        population.append(genom)
    
    return population

def evaluate_population(population):
    #for every member in population calculate cost
    population.sort(key = lambda x : cost(x))

def search_for_best_solution(population):
    best_child = population[0]
    while not stop_condition(best_child):
        parents = select_parents(population)
        children = produce_children(parents)
        evaluate_population(children)
        best_child = evaluate_best_child(children[0], best_child)
        population = replace_population(population, children)
    return best_child

def select_parents(population):
    #select some proportion of population to produce new population
    return select_best_parents_function(population)

def evaluate_best_child(child, current_best):
    if cost(child) <= cost(current_best):
        return child
    return current_best

def cost(child):
    #objective function for evaluating child
    return cost_function(child)

def produce_children(parents):
    #make parent pairs and cross them, than mutate children
    children = []
    parent_pairs = pair_parents(parents)
    for pair in  parent_pairs:
        child1, child2 = crossover(pair)
        child1 = mutate(child1)
        child2 = mutate(child2)
        children.append(child1)
        children.append(child2)
    return children

def pair_parents(parents):
    #generate parents pairs
    pairs = []
    for i in range(len(parents)//2):
        pairs.append([parents[i], parents[i + len(parents)//2]])
    return pairs
    
def crossover(parents):
    #select portion of each parent for child to be produced
    return crossover_domain_function(parents)

def mutate(child):
    #random change to child
     return mutation_domain_function(child)

def replace_population(population, children):
    #get portion of older generation and portion of children for new generation
    return domain_replace_population_function(population, children)

if __name__ == '__main__':
    crossover_rate = 0.98
    population_num = 100
    num_bits = 64
    mutation_rate = 1/num_bits
    iteration_num = 100
    print(genetic_alghorithm())