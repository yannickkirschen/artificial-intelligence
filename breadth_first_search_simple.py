def search(start, goal, next_states):
    frontier = {start}
    visited = set()
    parent = {start: start}

    while frontier:
        new_frontier = set()
        for s in frontier:
            for ns in next_states(s):
                if ns not in visited and ns not in frontier:
                    new_frontier.add(ns)
                    parent[ns] = s

                    if ns == goal:
                        return path_to(goal, parent)

        visited |= frontier
        frontier = new_frontier


def path_to(state, parent):
    p = parent[state]
    return [state] if p == state else path_to(p, parent) + [state]
