"""To what extent can you predict the weight of a player given his height and his age?"""

from csv import DictReader

import numpy as np
import linear_regression


def pos_to_num(pos: str) -> list[float]:
    match pos:
        case 'C':
            return [1, 0, 0]
        case 'G':
            return [0, 1, 0]
        case 'F':
            return [0, 0, 1]
        case _:
            raise ValueError(f'Unknown position: {pos}')


def read_csv(file: str) -> tuple[np.array, np.array]:
    with open(file) as f:
        reader = DictReader(f, delimiter=',')

        x = []
        y = []
        for row in reader:
            row = dict(row)  # fix typing

            height = float(row['Height'])
            age = float(row['Age'])
            pos = pos_to_num(row['Pos'])

            x.append([height, height ** 2, height ** 3, age, *pos] + [1.0])
            y.append(float(row['Weight']))
        return np.array(x), np.array(y)


def main():
    x, y = read_csv('nba.csv')

    r_squared = linear_regression.calc(x, y)
    print(f'R²: {r_squared}')


if __name__ == '__main__':
    main()
