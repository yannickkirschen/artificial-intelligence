'''
Backtrack Solver for CSPs. Copyright Prof. Dr. Karl Stroetmann.
'''

import ast
from typing import TypeVar

Value = TypeVar('Value')
Element = TypeVar('Element')
Variable = str
Formula = str
CSP = tuple[set[Variable] | list[Variable], set[Value], set[Formula]]
ACSP = tuple[set[Variable] | list[Variable], set[Value], list[tuple[Formula, set[Variable]]]]
Assignment = dict[Variable, Value]


def solve(p: CSP) -> Assignment | None:
    '''Solves a CSP using backtracking.'''

    variables, values, constraints = p
    csp = (variables, values, [(f, _collect_variables(f)) for f in constraints])
    return _backtrack_search({}, csp)


def all_different(v: set[str]) -> set[str]:
    '''Returns a set of constraints, stating that all variables in v must be different.'''
    return {f'{x} != {y}' for x in v
            for y in v
            if x < y
            }


def _collect_variables(expression: Formula) -> set[str]:
    tree = ast.parse(expression)
    return {node.id for node in ast.walk(tree)
            if isinstance(node, ast.Name)
            if node.id not in dir(__builtins__)
            }


def _is_consistent(var: Variable, value: Value, assignment: Assignment, constraints: list[tuple[Formula, set[Variable]]]) -> bool:
    new_assignment = assignment.copy()
    new_assignment[var] = value

    return all(eval(f, new_assignment) for (f, Vs) in constraints  # pylint: disable=W0123
               if var in Vs and Vs <= new_assignment.keys()
               )


def _backtrack_search(assignment: Assignment, p: ACSP) -> Assignment | None:
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
