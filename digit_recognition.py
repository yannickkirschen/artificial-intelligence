from sys import argv
from typing import List, Callable

import neural_network
import numpy as np


def sigmoid(x: int) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def sigmoid_prime(x: int) -> np.ndarray:
    s = sigmoid(x)
    return s * (1 - s)


def relu(x: int) -> np.ndarray:
    return np.maximum(0, x)


def relu_prime(x: int) -> np.ndarray:
    return np.where(x > 0, 1, 0)


def do_classic(epochs: int, training_data: List[np.ndarray], test_data: List[np.ndarray],
               func_h: Callable[[int], np.ndarray], func_prime_h: Callable[[int], np.ndarray],
               func_o: Callable[[int], np.ndarray], func_prime_o: Callable[[int], np.ndarray]):
    network = neural_network.Network(50, func_h, func_prime_h, func_o, func_prime_o)
    network.sgd(training_data, epochs, 10, 0.25, test_data)


def _do_ensemble(length: int, epochs: int, training_data: List[np.ndarray], test_data: List[np.ndarray]):
    ensemble = neural_network.Ensemble(length, epochs, training_data, test_data, relu, relu_prime, sigmoid,
                                       sigmoid_prime)
    ensemble.learn()
    print('Ensemble accuracy:', ensemble.evaluate(test_data))


def main():
    training_data, test_data = neural_network.load_data('./mnist.pkl.gz')
    np.random.seed(1)

    match argv[1:]:
        case ['relu', 'sigmoid']:
            do_classic(30, training_data, test_data, relu, relu_prime, sigmoid, sigmoid_prime)
        case ['sigmoid', 'relu']:
            do_classic(30, training_data, test_data, sigmoid, sigmoid_prime, relu, relu_prime)
        case ['relu']:
            do_classic(30, training_data, test_data, relu, relu_prime, sigmoid, sigmoid_prime)
        case ['ensemble', l, epochs]:
            _do_ensemble(int(l), int(epochs), training_data, test_data)
        case _:
            do_classic(30, training_data, test_data, sigmoid, sigmoid_prime, sigmoid, sigmoid_prime)


if __name__ == '__main__':
    main()
