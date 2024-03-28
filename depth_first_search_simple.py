def search(start, goal, next_states):
    stack = [start]
    parent = {start: start}

    while stack:
        state = stack.pop()
        for ns in next_states(state):
            if ns not in parent:
                parent[ns] = state

                if ns == goal:
                    return path_to(goal, parent)

                stack.append(ns)


def path_to(state, parent):
    path = [state]

    while state != parent[state]:
        state = parent[state]
        path = [state] + path

    return path
