'''
This implements Nim.

There are four rows of matches:
   - the first  row contains 1 match,
   - the second row contains 3 matches,
   - the third  row contains 5 matches, and
   - the fourth row contains 7 matches.

The player whose turn it is first selects a line. Then he takes any number of matches from this line.

The player that takes the last match has won the game.
'''

from functools import lru_cache
from os import system, name
from random import choice


Matches = tuple[int, ...]
State = tuple[Matches, str]


def _clear():
    system('cls' if name == 'nt' else 'clear')


@lru_cache(maxsize=None)
def _alpha_beta_max(s: State, alpha: int, beta: int, players: tuple[str, str]) -> int:
    if _finished(s):
        return _utility(s)

    for ns in _next_states(s, players[0]):
        value = _alpha_beta_min(ns, alpha, beta, players)
        if value >= beta:
            return value
        alpha = max(alpha, value)

    return alpha


@lru_cache(maxsize=None)
def _alpha_beta_min(s: State, alpha: int, beta: int, players: tuple[str, str]) -> int:
    if _finished(s):
        return _utility(s)

    for ns in _next_states(s, players[1]):
        value = _alpha_beta_max(ns, alpha, beta, players)
        if value <= alpha:
            return value
        beta = min(beta, value)

    return beta


def _best_move(s: State, players: tuple[str, str]) -> tuple[int, State]:
    next_states = _next_states(s, players[0])
    best_value = _alpha_beta_max(s, -1, 1, players)
    best_moves = [s for s in next_states if _alpha_beta_min(s, -1, 1, players) == best_value]
    best_state = choice(best_moves)
    return best_value, best_state


def _next_states(s: State, player: str) -> list[State]:
    matches, _ = s
    next_player = 'A' if player == 'B' else 'B'

    states = []
    for i, row in enumerate(matches):
        for j in range(1, row+1):
            new_state = matches[:i] + (row-j,) + matches[i+1:], next_player
            states.append(new_state)
    return states


def _utility(s: State) -> int | None:
    _, player = s
    if _finished(s):
        if player == 'A':
            return -1

        if player == 'B':
            return 1

        return 0  # Draw (not possible though)
    return None  # Not decided yet


def _finished(s: State) -> bool:
    return all(row == 0 for row in s[0])


def _get_move(s: State) -> State:
    matches, _ = s
    while True:
        try:
            row_str, count_str = input('Enter move with format "row, count": ').split(',')
            row, count = int(row_str), int(count_str)
            if 1 <= count <= matches[row]:
                new_matches = matches[:row] + (matches[row]-count,) + matches[row+1:]
                return (new_matches, 'A')

            print("Don't cheat! Please try again.")
        except ValueError:
            print('Illegal input.')


def _final_msg(s: State) -> bool:
    if _finished(s):
        if _utility(s) == -1:
            print('You have won!')
        elif _utility(s) == 1:
            print('The computer has won!')
        else:
            print("It's a draw.")
        return True
    return False


def _print_board(s: State):
    matches, _ = s

    _clear()
    for i, row in enumerate(matches):
        if row == 0:
            print(f'{i}: -')
        else:
            print(f'{i}: {"X " * row}')


def main():
    '''Play Nim.'''

    state: State = ((1, 3, 5, 7), 'A')
    players = ('A', 'B')

    while not _final_msg(state):
        val, state = _best_move(state, players)
        _print_board(state)
        print(f'For me, the game has the value {val}.')

        if _final_msg(state):
            return

        state = _get_move(state)
        _print_board(state)


if __name__ == '__main__':
    main()
