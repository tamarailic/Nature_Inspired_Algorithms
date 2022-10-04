import random
import math


def random_vector(minmax):
    return [minmax[i][0] + ((minmax[i][1] - minmax[i][0]) * random.random()) for i in range(len(minmax))]


def initialize_weights(problem_size):
    minmax = [[random.random(), random.random()]
              for _ in range(problem_size)]
    return random_vector(minmax)


def create_neuron(num_inputs):
    return {'weights': initialize_weights(num_inputs+1),
            'last_delta': [0] * (num_inputs + 1),
            'deriv': [0] * (num_inputs + 1)}


def activate(weights, vector):
    s = weights[len(weights) - 1] * 1
    for i, input in enumerate(vector):
        s += weights[i] * input
    return s


def transfer(activation):
    return 1.0 / (1.0 + math.exp(-activation))


def transfer_derivative(output):
    return output * (1.0 - output)


def forward_propagate(net, vector):
    for i, layer in enumerate(net):
        if i == 0:
            input = vector
        else:
            input = [net[i-1][k]['output'] for k in range(len(net[i - 1]))]
        for neuron in layer:
            neuron['activation'] = activate(neuron['weights'], input)
            neuron['output'] = transfer(neuron['activation'])
    return net[-1][0]['output']


def backward_propagate_error(network, expected_output):
    for n in range(len(network)):
        index = len(network) - 1 - n
        if index == len(network) - 1:
            neuron = network[index][0]
            error = (expected_output - neuron['output'])
            neuron['delta'] = error * transfer_derivative(neuron['output'])
        else:
            for k, neuron in enumerate(network[index]):
                sum = 0
                for next_neuron in network[index + 1]:
                    sum += (next_neuron['weights'][k] * next_neuron['delta'])
                neuron['delta'] = sum * transfer_derivative(neuron['output'])


def calculate_error_derivatives_for_weights(net, vector):
    for i, layer in enumerate(net):
        if i == 0:
            input = vector
        else:
            input = [net[i-1][k]['output'] for k in range(len(net[i - 1]))]
        for neuron in layer:
            for j, signal in enumerate(input):
                neuron['deriv'][j] += neuron['delta'] * signal
            neuron['deriv'][-1] += neuron['delta'] * 1.0


def update_weights(network, lrate, mom=0.8):
    for layer in network:
        for neuron in layer:
            for j, w in enumerate(neuron['weights']):
                delta = (lrate * neuron['deriv'][j]) + \
                    (neuron['last_delta'][j] * mom)
                neuron['weights'][j] += delta
                neuron['last_delta'][j] = delta
                neuron['deriv'][j] = 0.0


def train_network(network, domain, num_inputs, iterations, lrate):
    correct = 0
    for epoch in range(iterations):
        for pattern in domain:
            vector = [pattern[k] for k in range(num_inputs)]
            expected = pattern[-1]
            output = forward_propagate(network, vector)
            if round(output) == expected:
                correct += 1
            backward_propagate_error(network, expected)
            calculate_error_derivatives_for_weights(network, vector)
        update_weights(network, lrate)
        if (epoch+1) % 100 == 0:
            correct = 0


def test_network(network, domain, num_inputs):
    correct = 0
    for pattern in domain:
        input_vector = [pattern[k] for k in range(num_inputs)]
        output = forward_propagate(network, input_vector)
        if round(output) == pattern[-1]:
            correct += 1
    print(f"Finished test with a score of {correct}/{len(domain)}")
    return correct


def execute(domain, num_inputs, iterations, num_nodes, lrate):
    network = []
    network.append([create_neuron(num_inputs) for _ in range(num_nodes)])
    network.append([create_neuron(len(network[-1])) for _ in range(1)])
    train_network(network, domain, num_inputs, iterations, lrate)
    test_network(network, domain, num_inputs)
    return network


if __name__ == '__main__':
    xor = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    inputs = 2
    num_hidden_nodes = 4
    iterations = 2000
    learning_rate = 0.3
    execute(xor, inputs, iterations, num_hidden_nodes, learning_rate)
