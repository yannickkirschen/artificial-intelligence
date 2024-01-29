'''
Computes all solutions to the eight queens puzzle.
'''

State = tuple[int, ...]  # column where the queen is placed in each row


def check_diagonal(s: State) -> bool:
    '''Returns True if no two queens are on the same diagonal.'''

    for i, vi in enumerate(s):
        for j, vj in enumerate(s):
            if i == j:
                continue

            if i - j == abs(vi - vj):
                return False

    return True


def next_states(s: State) -> set[State]:
    '''Returns all possible states that can be reached from s.'''

    if len(s) == 8:
        return set()

    states = set()
    for col in range(8):
        next_state = s + (col,)
        if col not in s and check_diagonal(next_state):
            states.add(next_state)

    return states


def dfs(s: State, solutions: list[State]) -> None:
    '''Recursively computes all solutions to the eight queens puzzle using depth first search.'''

    if len(s) == 8:
        solutions.append(s)
        return

    for ns in next_states(s):
        dfs(ns, solutions)


def print_board(solution: State) -> None:
    '''Prints the chess board with the given solution.'''

    for row in range(8):
        for col in range(8):
            if col == solution[row]:
                print(' Q', end='')
            else:
                print(' ·', end='')
        print()


def main():
    '''Main function.'''

    start: State = ()
    solutions: list[State] = []
    dfs(start, solutions)

    print(' +++ Eight queens puzzle +++')
    print(f'The upper bound of possible states is {8 ** 8}.')
    print(f'There are {len(solutions)} solutions.')
    print('One of them is:')
    print_board(solutions[0])


if __name__ == '__main__':
    main()
