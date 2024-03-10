from collections import deque
from typing import TypeVar, Callable

State = TypeVar('State')


def search(start: State, goal: State, next_states: Callable[[State], set[State]]) -> list[State] | None:
    frontier = deque([start])
    parent = {start: start}

    while frontier:
        state = frontier.popleft()
        if state == goal:
            return path_to(state, parent)

        for ns in next_states(state):
            if ns not in parent:
                parent[ns] = state
                frontier.append(ns)

    return None


def path_to(state: State, parent: dict[State, State]) -> list[State]:
    p = parent[state]
    return [state] if p == state else path_to(p, parent) + [state]
