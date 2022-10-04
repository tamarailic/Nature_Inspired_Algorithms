import random
import re


def random_bitstring():
    bitstring = ''
    for _ in range(num_bits):
        random_chance = random.random()
        if random_chance >= 0.5:
            bitstring += '1'
        else:
            bitstring += '0'

    return bitstring


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population) - 1)
    while i == j:
        j = random.randint(0, len(population) - 1)
    if population[i]['fitness'] < population[j]['fitness']:
        return population[i]
    return population[j]


def point_mutation(bitstring):
    mutated_child = ''

    for i in range(len(bitstring)):
        random_chance = random.random()
        if random_chance < 1/len(bitstring):
            if bitstring[i] == '1':
                mutated_child += '0'
            else:
                mutated_child += '1'
        else:
            mutated_child += bitstring[i]
    return mutated_child


def one_point_crossover(p1, p2):
    if random.random() > p_cross:
        return '' + p1['bitstring']
    cut = random.randrange(
        0, min(len(p1['bitstring']), len(p2['bitstring'])/codon_bits))
    cut *= codon_bits
    return p1['bitstring'][:cut] + p2['bitstring'][cut:]


def codon_duplication(bitstring):
    if random.random() > 1/codon_bits:
        return bitstring
    codons = len(bitstring) // codon_bits
    rand_num = random.randrange(0, codons - 1)
    return bitstring + bitstring[rand_num * codon_bits: rand_num * codon_bits + codon_bits]


def codon_deletion(bitstring):
    if random.random() > 1/codon_bits:
        return bitstring
    codons = len(bitstring) // codon_bits
    off = random.randint(0, codons) * codon_bits
    return bitstring[:off] + bitstring[off + codon_bits: len(bitstring)]


def reproduce(selected):
    children = []
    for i in range(len(selected)):
        if i == len(selected)-1:
            p2 = selected[0]
        elif i % 2 == 0:
            p2 = selected[i+1]
        else:
            p2 = selected[i-1]
        child = {}
        child['bitstring'] = one_point_crossover(selected[i], p2)
        child['bitstring'] = codon_deletion(child['bitstring'])
        child['bitstring'] = codon_duplication(child['bitstring'])
        child['bitstring'] = point_mutation(child['bitstring'])
        children.append(child)
        if len(children) == pop_size:
            break
    return children


def decode_integers(bitstring):
    ints = []
    for off in range(len(bitstring)//codon_bits):
        codon = bitstring[off * codon_bits: off * codon_bits + codon_bits]
        sum = 0
        for i in range(len(codon)):
            sum += (1 if codon[i] == '1' else 0) * (2 ** i)
        ints.append(sum)
    return ints


def map_integers(integers):
    done, offset, current_depth = False, 0, 0
    symbolic_string = grammar['S']

    while True:
        done = True
        for key in grammar.keys():
            occurences = re.findall(key, symbolic_string)
            for occurence in occurences:
                done = False
                if occurence == 'EXP' and current_depth >= max_depth - 1:
                    set = grammar['VAR']
                else:
                    set = grammar[occurence]
                integer = integers[offset] % len(set)
                offset = 0 if offset == len(integers) - 1 else offset + 1
                symbolic_string = symbolic_string.replace(
                    occurence, set[integer], 1)
        current_depth += 1
        if done:
            break

    return symbolic_string


def init_population():
    population = []
    for _ in range(pop_size):
        member = {}
        member['bitstring'] = random_bitstring()
        population.append(member)
    return population


def evaluate_population(population):
    for i in range(len(population)):
        evaluate(population[i])
    return population


def evaluate(member):
    member['integers'] = decode_integers(member['bitstring'])
    member['program'] = map_integers(member['integers'])
    member['fitness'] = cost(member['program'])


def cost(program, num_trails=30):
    if program.strip() == 'INPUT':
        return 9999999

    sum_error = 0
    for _ in range(num_trails):
        x = sample_from_bounds()
        expression = re.sub('INPUT', str(x), program)
        try:
            score = eval(expression)
        except:
            return 9999999
        sum_error += abs(score - target_function(x))
    return sum_error / num_trails


def target_function(x):
    return x**4 + x**3 + x**2 + x


def sample_from_bounds():
    return bounds[0] + ((bounds[1] - bounds[0]) * random.random())


def search():
    population = init_population()
    population = evaluate_population(population)
    best = population[0]

    for _ in range(max_gens):
        selected = []
        for _ in range(pop_size):
            selected.append(binary_tournament(population))
        children = reproduce(selected)
        children = evaluate_population(children)
        children = sorted(children, key=lambda x: x['fitness'])
        if children[0]['fitness'] <= best['fitness']:
            best = children[0]
        population = children + population
        population = sorted(population, key=lambda x: x['fitness'])[:pop_size]
        if best['fitness'] == 0:
            break
    return best


if __name__ == '__main__':
    grammar = {'S': 'EXP',
               'EXP': [' EXP BINARY EXP ', ' (EXP BINARY EXP) ', ' VAR '],
               'BINARY': ['+', '-', '/', '*'],
               'VAR': ['INPUT', '1.0']}
    bounds = [1, 10]
    max_depth = 7
    max_gens = 50
    pop_size = 100
    codon_bits = 4
    num_bits = 10 * codon_bits
    p_cross = 0.3
    best = search()
    print(best['fitness'], best['program'])
