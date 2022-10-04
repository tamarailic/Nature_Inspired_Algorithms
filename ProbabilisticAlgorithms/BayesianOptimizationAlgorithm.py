import random


def random_bitstring(num_bits):
    bitstring = []
    for _ in range(num_bits):
        if random.random() < 0.5:
            bitstring.append(1)
        else:
            bitstring.append(0)
    return bitstring


def onemax(vector):
    return sum(vector)


def path_exists(i, j, graph):
    visited, stack = [], [i]
    while stack != []:
        if j in stack:
            return True
        k = stack.pop()
        if k in visited:
            continue
        visited.append(k)
        for m in graph[k]['out']:
            if m not in visited:
                stack.append(m)
    return False


def can_add_edge(i, j, graph):
    return j not in graph[i]['out'] and not path_exists(j, i, graph)


def get_viable_parents(node, graph):
    viable = []
    for i in range(len(graph)):
        if node != i and can_add_edge(node, i, graph):
            viable.append(i)
    return viable


def fact(v):
    if v <= 1:
        return 1
    else:
        return v*fact(v-1)


def compute_count_for_edges(pop, indexes):
    counts = [0] * 2**(len(indexes))
    for p in pop:
        index = 0
        for i, v in enumerate(list(reversed(indexes))):
            if p['bitstring'][v] == 1:
                index += 1 * (2**i)
        counts[index] += 1

    return counts


def k2equation(node, candidates, pop):
    counts = compute_count_for_edges(pop, [node]+candidates)
    total = None
    for i in range(len(counts)//2):
        a1, a2 = counts[i * 2], counts[i * 2 + 1]
        rs = (1.0/fact((a1+a2)+1)) * fact(a1) * fact(a2)
        if total == None:
            total = rs
        else:
            total *= rs
    return total


def compute_gains(node, graph, pop, max=2):
    viable = get_viable_parents(node['num'], graph)
    gains = [-1 for i in range(len(graph))]
    for i in range(len(gains)):
        if len(graph[i]['in']) < max and i in viable:
            gains[i] = k2equation(node['num'], node['in']+[i], pop)
    return gains


def construct_network(pop, prob_size, max_edges=None):
    if max_edges == None:
        max_edges = 3*len(pop)
    graph = [{'out': [], 'in':[], 'num':i} for i in range(prob_size)]
    gains = [0] * prob_size
    for _ in range(max_edges):
        maxi, from_where, to = -1, None, None
        for i, node in enumerate(graph):
            gains[i] = compute_gains(node, graph, pop)
            for j, v in enumerate(gains[i]):
                if v > maxi:
                    from_where, to, maxi = i, j, v
        if maxi <= 0:
            break
        graph[from_where]['out'].append(to)
        graph[to]['in'].append(from_where)
    return graph


def topological_ordering(graph):
    for n in graph:
        n['count'] = len(n['in'])
    ordered, stack = [], [n for n in graph if n['count'] == 0]
    while len(ordered) < len(graph):
        current = stack.pop()
        for edge in current['out']:
            for n in graph:
                if n['num'] == edge:
                    node = n
                    node['count'] -= 1
                    if node['count'] <= 0:
                        stack.append(node)

        ordered.append(current)
    return ordered


def marginal_probability(i, pop):
    return sum([x['bitstring'][i] for x in pop]) / len(pop)


def calculate_probability(node, bitstring, graph, pop):
    if node['in'] == []:
        return marginal_probability(node['num'], pop)
    counts = compute_count_for_edges(pop, [node['num']]+node['in'])
    index = 0
    for i, v in enumerate(list(reversed(node['in']))):
        if bitstring[v] == 1:
            index += 1 * (2**i)

    i1 = index + (1*2**(len(node['in'])))
    i2 = index
    a1, a2 = counts[i1], counts[i2]
    try:
        return a1/(a1+a2)
    except Exception:
        return 1


def probabilistic_logic_sample(graph, pop):
    bitstring = [0] * len(graph)
    for node in graph:
        prob = calculate_probability(node, bitstring, graph, pop)
        if random.random() < prob:
            bitstring[node['num']] = 1
        else:
            bitstring[node['num']] = 0
    return {'bitstring': bitstring}


def sample_from_network(pop, graph, num_samples):
    ordered = topological_ordering(graph)
    samples = [probabilistic_logic_sample(
        ordered, pop) for _ in range(num_samples)]
    return samples


def search(num_bits, max_iter, pop_size, select_size, num_children):
    pop = [{'bitstring': random_bitstring(num_bits)} for _ in range(pop_size)]
    for p in pop:
        p['cost'] = onemax(p['bitstring'])
    best = sorted(pop, key=lambda x: x['cost'], reverse=True)[0]
    for _ in range(max_iter):
        selected = pop[:select_size]
        network = construct_network(selected, num_bits)
        arcs = sum([len(x['out']) for x in network])
        children = sample_from_network(selected, network, num_children)
        for child in children:
            child['cost'] = onemax(child['bitstring'])
        pop = pop[:(pop_size - select_size)] + children
        pop = sorted(pop, key=lambda x: x['cost'], reverse=True)
        if pop[0]['cost'] >= best['cost']:
            best = pop[0]
        if [x for x in pop if x['bitstring'] != pop[0]['bitstring']] == []:
            converged = True
        else:
            converged = False
        if converged or best['cost'] == num_bits:
            break
    return best


if __name__ == '__main__':
    num_bits = 20
    max_iter = 100
    pop_size = 50
    select_size = 15
    num_children = 25
    best = search(num_bits, max_iter, pop_size, select_size, num_children)
    print(best['cost'])
