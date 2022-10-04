import math
import random


def rand_in_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound - lower_bound) * random.random()


def generate_random_program(depth=0):
    if depth == max_depth - 1 or (depth > 1 and random.random() < 0.1):
        term = terms[random.randint(0, len(terms) - 1)]
        if term == 'R':
            return rand_in_bounds(-5, 5)
        return term

    depth += 1
    arg1 = generate_random_program(depth)
    arg2 = generate_random_program(depth)
    return [funcs[random.randint(0, len(funcs) - 1)], arg1, arg2]


def generate_random_programs():
    population = []
    for _ in range(pop_size):
        program = {'prog': generate_random_program(),
                   'fitness': -1}
        population.append(program)

    return population


def calculate_programs_fitness(programs):
    for program in programs:
        program['fitness'] = fitness(program['prog'])
    return programs


def fitness(program, num_trails=20):
    sum_error = 0.0
    for _ in range(num_trails):
        input = rand_in_bounds(-1, 1)
        error = eval_program(program, input) - target_function(input)
        sum_error += abs(error)

    return sum_error / num_trails


def eval_program(program, input):
    if type(program) != list:
        if program == 'X':
            return input
        return program

    arg1, arg2 = eval_program(
        program[1], input), eval_program(program[2], input)
    if program[0] == '/' and arg2 == 0:
        return 0
    return calculate_expression(program[0], arg1, arg2)


def calculate_expression(operation, arg1, arg2):

    if arg2 == 0:
        return 0
    elif operation == '+':
        return arg1 + arg2
    elif operation == '-':
        return arg1 - arg2
    elif operation == '*':
        return arg1 * arg2
    else:
        return arg1 / arg2


def target_function(input):
    return input ** 2 + input + 1


def tournament_selection(population):
    selected = []
    for _ in range(bouts):
        selected.append(population[random.randint(0, len(population) - 1)])
    return sorted(selected, key=lambda x: x['fitness'])[0]


def crossover(parent1, parent2):
    try:
        point1 = random.randint(0, count_nodes(parent1) - 2) + 1
    except:
        point1 = 1

    try:
        point2 = random.randint(0, count_nodes(parent2) - 2) + 1
    except:
        point2 = 1
    tree1, _ = get_node(parent1, point1)
    tree2, _ = get_node(parent2, point2)
    child1, _ = replace_node(parent1, tree2, point1)
    child1 = prune(child1)
    child2, _ = replace_node(parent2, tree1, point2)
    child2 = prune(child2)
    return [child1, child2]


def count_nodes(parent):
    if type(parent) != list:
        return 1
    a1 = count_nodes(parent[1])
    a2 = count_nodes(parent[2])
    return a1 + a2 + 1


def get_node(node, node_num, current_node=0):
    if current_node == node_num:
        return node
    node_num += 1
    if type(node) != list:
        return 0, current_node

    a1, current_node = get_node(node[1], node_num, current_node)
    if a1 != None:
        return a1, current_node

    a2, current_node = get_node(node[2], node_num, current_node)
    if a2 != None:
        return a2, current_node

    return 0, current_node


def replace_node(node, replacement, node_num, curr_node=0):
    if curr_node == node_num:
        return [replacement, curr_node + 1]
    curr_node += 1

    if type(node) != list:
        return [node, curr_node]

    a1, curr_node = replace_node(node[1], replacement, node_num, curr_node)
    a2, curr_node = replace_node(node[2], replacement, node_num, curr_node)

    return [[node[0], a1, a2], curr_node]


def prune(node, depth=0):
    if depth == max_depth - 1:
        term = terms[random.randint(0, len(terms) - 1)]
        if term == 'R':
            return rand_in_bounds(-5, 5)
        return term

    depth += 1
    if type(node) != list:
        return node

    a1 = prune(node[1])
    a2 = prune(node[2])

    return [node[0], a1, a2]


def mutation(parent):
    random_tree = generate_random_program(depth=max_depth // 2)
    point = random.randint(0, count_nodes(parent))
    child, _ = replace_node(parent, random_tree, point)
    child = prune(child)
    return child


def search():
    population = generate_random_programs()
    population = calculate_programs_fitness(population)
    best = sorted(population, key=lambda x: x['fitness'])[0]
    for _ in range(max_gens):

        children = []
        while len(children) < pop_size:

            operation = random.random()
            program1 = tournament_selection(population)
            copy_program1 = {}

            if operation < p_repro:
                copy_program1['prog'] = program1['prog']
            if operation < p_repro + p_cross:
                program2 = tournament_selection(population)
                copy_program2 = {}
                copy_program1['prog'], copy_program2['prog'] = crossover(
                    program1['prog'], program2['prog'])
                children.append(copy_program2)
            if operation < p_repro + p_cross + p_mut:
                copy_program1['prog'] = mutation(program1['prog'])

            if len(children) < pop_size:
                children.append(copy_program1)

        children = calculate_programs_fitness(children)
        population = children
        population_best = sorted(population, key=lambda x: x['fitness'])[0]

        if population_best['fitness'] <= best['fitness']:
            best = population_best

        if best['fitness'] == 0:
            break

    return best


if __name__ == '__main__':
    terms = ['X', 'R']
    funcs = ['+', '-', '*', '/']
    max_gens = 100
    max_depth = 7
    pop_size = 100
    bouts = 5
    p_repro = 0.08
    p_cross = 0.9
    p_mut = 0.02
    best = search()
    print(best['fitness'])
