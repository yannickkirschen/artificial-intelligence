'''
Taoistic Search for the 15-puzzle.
'''

import heapq
from typing import Callable


Row = tuple[str, ...]
State = tuple[Row, ...]
Move = tuple[int, int]

NxtStFct = Callable[[State], set[State]]
Heuristic = Callable[[State, State], int]


def _find_tile(tile: str, s: State) -> tuple[int, int] | None:
    n = len(s)
    for row in range(n):
        for col in range(n):
            if s[row][col] == tile:
                return row, col
    return None


def _to_list(s: State) -> list[list[str]]:
    return [list(row) for row in s]


def _to_tuple(s: list[list[str]]) -> State:
    return tuple(tuple(row) for row in s)


def _move_dir(s: State, row: int, col: int, dx: int, dy: int) -> State:
    s = _to_list(s)
    s[row][col] = s[row + dy][col + dx]
    s[row + dy][col + dx] = '0'
    return _to_tuple(s)


def _next_states(s: State) -> set[State]:
    n = len(s)
    row, col = _find_tile('0', s)
    new_states = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        if row + dy in range(n) and col + dx in range(n):
            new_states.add(_move_dir(s, row, col, dx, dy))

    return new_states


def _matches(pattern: State, s: State) -> bool:
    for i, single_pattern in enumerate(pattern):
        for j, char in enumerate(single_pattern):
            if char not in ('*', s[i][j]):
                return False

    return True


def _manhattan(s1: State, s2: State) -> int:
    n = len(s1)
    result = 0
    for row in range(n):
        for col in range(n):
            tile = s1[row][col]
            if tile not in ('*', '0'):
                pos = _find_tile(tile, s2)
                if pos:
                    r, c = pos
                    result += abs(row - r) + abs(col - c)

    return result


def _find_numbers(pattern: State) -> list[str]:
    result = []
    n = len(pattern)
    for row in range(n):
        for col in range(n):
            tile = pattern[row][col]
            if tile != '*':
                result.append(tile)

    return result


def _replace_numbers(pattern: State, tiles: list[str]) -> State:
    state: State = ()
    for row in pattern:
        new_row: Row = ()
        for col in row:
            if col not in tiles:
                new_row += ('*',)
            else:
                new_row += (col,)

        state += (new_row,)

    return state


def _intermediate_goals(goal: State, tiles: list[list[str]]) -> list[State]:
    goals: list[State] = []
    all_goals: list[str] = []
    for tile in tiles:
        all_goals += tile
        goals.append(_replace_numbers(goal, all_goals))

    return goals


def _extract_move(p1: State, p2: State) -> Move:
    r1, c1 = _find_tile('0', p1)
    r2, c2 = _find_tile('0', p2)
    return c2 - c1, r2 - r1


def _extract_move_list(patterns: list[State]) -> list[Move]:
    moves = []
    for index in range(len(patterns) - 1):
        moves.append(_extract_move(patterns[index], patterns[index + 1]))

    return moves


def _apply_move_list(s: State, moves: list[Move]) -> list[State]:
    states = [s]
    for move in moves:
        new_state = _move_dir(states[-1], *_find_tile('0', states[-1]), *move)
        states.append(new_state)

    return states


def _state_to_string(s: State) -> str:
    n = len(s)
    indent = " " * 4
    line = indent + "+---" * n + "+\n"
    result = line
    for row in range(n):
        result += indent + "|"
        for col in range(n):
            cell = s[row][col]
            if isinstance(cell, str) and cell != '*':
                number = int(cell)

            if cell == "*":
                result += " * "
            elif number >= 10:
                result += str(cell) + " "
            elif 0 < number < 10:
                result += " " + cell + " "
            else:
                result += "   "
            result += "|"
        result += "\n"
        result += line
    return result


def _search(start: State, goal: State, next_states: NxtStFct, heuristic: Heuristic) -> list[State] | None:
    visited: set[State] = set()
    priority_queue = [(heuristic(start, goal), [start])]
    while len(priority_queue) > 0:
        _, path = heapq.heappop(priority_queue)
        state = path[-1]
        if state in visited:
            continue
        if _matches(goal, state):
            print(f'Number of states visited: {len(visited)}')
            return path
        for ns in next_states(state):
            if ns not in visited:
                priority = heuristic(ns, goal) + len(path)
                heapq.heappush(priority_queue, (priority, path + [ns]))
        visited.add(state)
    return None


def _draw_state(s: State) -> None:
    print(_state_to_string(s))


def _shorten(solution: list[State]) -> list[State]:
    shorter = []
    k = 0
    while k < len(solution) - 1:
        shorter.append(solution[k])
        if k + 2 < len(solution) and solution[k] == solution[k + 2]:
            k += 3
        else:
            k += 1
    shorter += [solution[-1]]
    return shorter


def _main(start: State, goal: State) -> list[State] | None:
    tiles = [['14', '15'],
             ['12', '13'],
             ['10', '11'],
             ['8',  '9'],
             ['3',  '7'],
             ['2',  '6'],
             ['0', '1', '4', '5']
             ]
    patterns = _intermediate_goals(goal, tiles)
    state = start
    solution = []

    print('Start state:')
    _draw_state(start)
    for pattern in patterns:
        print('Trying to reach the following pattern:')
        _draw_state(pattern)
        tiles = _find_numbers(pattern)
        extended_state = _replace_numbers(state, tiles + ['0'])
        path = _search(extended_state, pattern, _next_states, _manhattan)

        print(path)
        if path:
            moves = _extract_move_list(path)
            path = _apply_move_list(state, moves)
            print(f'The following state is reached after {len(path)-1} steps:')
            state = path[-1]
            _draw_state(state)
            solution += path[:-1]
        else:
            return None
    solution += [goal]
    return solution


if __name__ == '__main__':
    start_state: State = (
        ('0', '14',  '8', '12'),
        ('10', '11', '13',  '9'),
        ('6',  '2',  '4', '15'),
        ('3',  '5',  '7',  '1')
    )

    goal_state: State = (
        ('0',  '1',  '2',  '3'),
        ('4',  '5',  '6',  '7'),
        ('8',  '9', '10', '11'),
        ('12', '13', '14', '15')
    )

    Path = _main(start_state, goal_state)
    if Path:
        print(len(Path)-1)
        print(len(_shorten(Path)) - 1)
        print(_shorten(Path))
