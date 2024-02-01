'''
Backtrack Solver for CSPs. Copyright Prof. Dr. Karl Stroetmann.
'''

import ast
from typing import TypeVar

Value = TypeVar('Value')
Element = TypeVar('Element')
CSP = tuple[set[str] | list[str], set[Value], set[str]]
ACSP = tuple[set[str] | list[str], set[Value], list[tuple[str, set[str]]]]
Assignment = dict[str, Value]
Solution = dict[str, Value]


def all_different(v: set[str]) -> set[str]:
    '''Returns a set of constraints, stating that all variables in v must be different.'''
    return {f'{x} != {y}' for x in v
            for y in v
            if x < y
            }


def _collect_variables(expression: str) -> set[str]:
    tree = ast.parse(expression)
    return {node.id for node in ast.walk(tree)
            if isinstance(node, ast.Name)
            if node.id not in dir(__builtins__)
            }


def _is_consistent(var: str, value: Value, assignment: dict[str, Value], constraints: list[tuple[str, set[str]]]) -> bool:
    new_assign = assignment.copy()
    new_assign[var] = value

    return all(eval(f, new_assign) for (f, Vs) in constraints if var in Vs and Vs <= new_assign.keys())  # pylint: disable=W0123


def _backtrack_search(assignment: dict[str, Value], p: ACSP) -> Solution | None:
    variables, values, constraints = p
    if len(assignment) == len(variables):
        return assignment

    if isinstance(variables, set):
        s = variables - assignment.keys()
        var = s.pop() if s else None
    else:  # if Variables is a list we choose the first unassigned variable
        var = [x for x in variables if x not in assignment][0]
    for value in values:
        if _is_consistent(var, value, assignment, constraints):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            solution = _backtrack_search(new_assignment, p)

            if solution is not None:
                return solution

    return None


def solve(p: CSP) -> Solution | None:
    '''Solves a CSP using backtracking.'''

    variables, values, constraints = p
    csp = (variables, values, [(f, _collect_variables(f)) for f in constraints])
    return _backtrack_search({}, csp)
