import csv
from math import pi

import numpy as np

import linear_regression


def read_csv(file: str) -> (np.array, np.array):
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')

        x = []
        y = []
        for row in reader:
            row = dict(row)  # fix typing

            # V = π · r^2 · h
            x.append([(float(row['Diameter']) / 2) ** 2 * float(row['Height']) * pi] + [1.0])
            y.append(float(row['Volume']))
        return np.array(x), np.array(y)


def main():
    x, y = read_csv('chainsaw-massacre.csv')

    r_squared = linear_regression.calc(x, y)
    print(f'R²: {r_squared}')


if __name__ == '__main__':
    main()
