from typing import TypeVar, Callable

State = TypeVar('State')


def search(start: State, goal: State, next_states: Callable[[State], set[State]]) -> list[State] | None:
    return dfs(start, goal, next_states, [start], {start})


def dfs(state: State,
        goal: State,
        next_states: Callable[[State], set[State]],
        path: list[State],
        path_set: set[State]) -> list[State] | None:
    if state == goal:
        return path

    for ns in next_states(state):
        if ns not in path_set:
            result = dfs(ns, goal, next_states, path + [ns], path_set | {ns})
            if result:
                return result

    return None
