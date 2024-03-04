import numpy as np


def calc(x: np.array, y: np.array) -> float:
    w = np.linalg.solve(x.T @ x, x.T @ y)

    rss = np.sum((x @ w - y) ** 2)
    y_mean = np.mean(y)
    tss = np.sum((y - y_mean) ** 2)

    return 1 - rss / tss
