import gzip
import pickle
import random
from typing import Callable, Any, List

import numpy as np


def vectorized_result(d):
    e = np.zeros((10, 1), dtype=np.float32)
    e[d] = 1.0
    return e


def load_data(file: str):
    with gzip.open(file, 'rb') as f:
        train, _, test = pickle.load(f, encoding="latin1")
    print(f'shape of training data: {(train[0].shape, train[1].shape)}')
    training_inputs = [np.reshape(x, (784, 1)) for x in train[0]]
    training_results = [vectorized_result(y) for y in train[1]]
    training_data = list(zip(training_inputs, training_results))
    test_inputs = [np.reshape(x, (784, 1)) for x in test[0]]
    test_data = list(zip(test_inputs, test[1]))
    return training_data, test_data


def random_matrix(rows, cols):
    return np.random.randn(rows, cols) / np.sqrt(cols)


class Network:
    def __init__(self, hidden_size, func_h: Callable[[int], np.ndarray], func_prime_h: Callable[[int], np.ndarray],
                 func_o: Callable[[int], np.ndarray], func_prime_o: Callable[[int], np.ndarray]):
        self.mInputSize = 28 * 28
        self.mHiddenSize = hidden_size
        self.mOutputSize = 10

        self.mBiasesH = np.zeros((self.mHiddenSize, 1))  # biases hidden layer
        self.mBiasesO = np.zeros((self.mOutputSize, 1))  # biases output layer
        self.mWeightsH = random_matrix(self.mHiddenSize, self.mInputSize)  # weights hidden layer
        self.mWeightsO = random_matrix(self.mOutputSize, self.mHiddenSize)  # weights output layer

        self.func_h = func_h
        self.func_prime_h = func_prime_h

        self.func_o = func_o
        self.func_prime_o = func_prime_o

    def feedforward(self, x):
        ah = self.func_h(self.mWeightsH @ x + self.mBiasesH)  # hidden layer
        ao = self.func_o(self.mWeightsO @ ah + self.mBiasesO)  # output layer
        return ao

    def sgd(self, training_data, epochs, mbs, alpha, test_data):
        n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mbs] for k in range(0, n, mbs)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, alpha)
            print('Epoch %2d: %d / %d' % (j, self.evaluate(test_data), n_test))

    def update_mini_batch(self, mini_batch, alpha):
        nabla_bh = np.zeros((self.mHiddenSize, 1))  # gradient of biases  of hidden layer
        nabla_bo = np.zeros((self.mOutputSize, 1))  # gradient of biases  of output layer
        nabla_wh = np.zeros((self.mHiddenSize, self.mInputSize))  # gradient of weights of hidden layer
        nabla_wo = np.zeros((self.mOutputSize, self.mHiddenSize))  # gradient of weights of output layer

        for x, y in mini_batch:
            dlt_nbl_bh, dlt_nbl_bo, dlt_nbl_wh, dlt_nbl_wo = self.backprop(x, y)
            nabla_bh += dlt_nbl_bh
            nabla_bo += dlt_nbl_bo
            nabla_wh += dlt_nbl_wh
            nabla_wo += dlt_nbl_wo

        alpha /= len(mini_batch)  # rescale learning rate
        self.mBiasesH -= alpha * nabla_bh
        self.mBiasesO -= alpha * nabla_bo
        self.mWeightsH -= alpha * nabla_wh
        self.mWeightsO -= alpha * nabla_wo

    def backprop(self, x, y):
        # feedforward pass
        zh = self.mWeightsH @ x + self.mBiasesH
        ah = self.func_h(zh)

        zo = self.mWeightsO @ ah + self.mBiasesO
        ao = self.func_o(zo)

        # backwards pass, output layer
        epsilon_0 = (ao - y) * self.func_prime_o(zo)
        nabla_bo = epsilon_0
        nabla_wo = epsilon_0 @ ah.transpose()

        # backwards pass, hidden layer
        epsilon_h = (self.mWeightsO.transpose() @ epsilon_0) * self.func_prime_h(zh)
        nabla_bh = epsilon_h
        nabla_wh = epsilon_h @ x.transpose()
        return nabla_bh, nabla_bo, nabla_wh, nabla_wo

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y) for x, y in test_data]
        return sum(y1 == y2 for y1, y2 in test_results)


def most_common(lst: List[Any]):
    return max(set(lst), key=lst.count)


class Ensemble:
    _l: int
    _epochs: int
    _training_data: List[np.ndarray]
    _test_data: List[np.ndarray]

    _networks: List[Network] = []

    _func_h: Callable[[int], np.ndarray]
    _func_prime_h: Callable[[int], np.ndarray]

    _func_o: Callable[[int], np.ndarray]
    _func_prime_o: Callable[[int], np.ndarray]

    def __init__(self, length: int, epochs: int, training_data: List[np.ndarray], test_data: List[np.ndarray],
                 func_h: Callable[[int], np.ndarray], func_prime_h: Callable[[int], np.ndarray],
                 func_o: Callable[[int], np.ndarray], func_prime_o: Callable[[int], np.ndarray]):
        super().__init__()

        self._l = length
        self._epochs = epochs
        self._training_data = training_data
        self._test_data = test_data

        self._func_h = func_h
        self._func_prime_h = func_prime_h

        self._func_o = func_o
        self._func_prime_o = func_prime_o

    def learn(self) -> List[Network]:
        for _ in range(self._l):
            print(f'Learning network {_ + 1} of {self._l}')
            network = Network(50, self._func_h, self._func_prime_h, self._func_o, self._func_prime_o)
            network.sgd(self._training_data, self._epochs, 10, 0.25, self._test_data)
            self._networks.append(network)

        return self._networks

    def evaluate(self, test_data: List[np.ndarray]) -> int:
        results = []
        for network in self._networks:
            test_results = [(np.argmax(network.feedforward(x)), y) for (x, y) in test_data]
            results.append(sum(int(x == y) for (x, y) in test_results))
        return most_common(results)
