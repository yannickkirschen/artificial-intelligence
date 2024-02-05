'''
The following puzzle is known as the Zebra Puzzle and was featured in the magazine Life International on
December 17, 1962. It presents a series of clues pertaining to the occupants of five distinct houses, challenging the
solver to deduce specific details about them. The puzzle is structured as follows:

1. There are five houses.
2. The Englishman lives in the red house. 3. The Spaniard owns the dog.
4. Coffee is drunk in the green house.
5. The Ukrainian drinks tea.
6. The green house is immediately to the right of the ivory house.
7. The Old Gold smoker owns snails.
8. Kools are smoked in the yellow house.
9. Milk is drunk in the middle house.
10. The Norwegian lives in the first house.
11. The man who smokes Chesterfields lives in the house next to the man with the fox.
12. Kools are smoked in the house next to the house where the horse is kept.
13. The Lucky Strike smoker drinks orange juice.
14. The Japanese smokes Parliaments.
15. The Norwegian lives next to the blue house.

The following facts are also given:
1. Each of the five houses is painted a unique color.
2. The residents of the five houses each have a distinct nationality.
3. A different pet is kept in each house.
4. The beverages consumed in the various houses are all unique.
5. A distinct brand of cigarettes is smoked in each house.

The objective of the Zebra Puzzle is to answer the following two questions:
    1. Who drinks water?
    2. Who owns the zebra?

Next, we formulate the zebra puzzle as a constraint satisfaction problem.
'''

from dataclasses import dataclass

from tabulate import tabulate

from backtrack_solver import CSP, Assignment, all_different, solve

from zebra2 import solve as solve2


@dataclass
class _Zebra:
    nations: set[str]
    drinks: set[str]
    pets: set[str]
    brands: set[str]
    colors: set[str]


def _print_solution(solution: Assignment, data: _Zebra) -> None:
    houses: list[list[str]] = []

    for i in range(1, 5+1):
        house: list[str] = [f'{i}']
        for _class in [data.nations, data.drinks, data.pets, data.brands, data.colors]:
            for x in _class:
                if solution[x] == i:
                    house.append(x)
        houses.append(house)

    print(tabulate(houses, headers=['House', 'Nation', 'Drink', 'Pet', 'Brand', 'Color'], tablefmt='pretty'))
    print()

    for house in houses:
        if house[2] == 'Water':
            print(f'{house[1]} drinks water')
        if house[3] == 'Zebra':
            print(f'{house[1]} owns the zebra')


def main():
    '''Main function for the zebra puzzle.'''

    nations = {'English', 'Spanish', 'Ukrainian', 'Norwegian', 'Japanese'}
    drinks = {'Coffee', 'Tea', 'Milk', 'OrangeJuice', 'Water'}
    pets = {'Dog', 'Snails', 'Horse', 'Fox', 'Zebra'}
    brands = {'LuckyStrike', 'Parliaments', 'Kools', 'Chesterfields', 'OldGold'}
    colors = {'Red', 'Green', 'Ivory', 'Yellow', 'Blue'}

    variables = nations | drinks | pets | brands | colors
    values = {1, 2, 3, 4, 5}
    constraints = {'English       == Red',           # The Englishman lives in the red house.
                   'Spanish       == Dog',           # The Spaniard owns the dog.
                   'Coffee        == Green',         # Coffee is drunk in the green house.
                   'Ukrainian     == Tea',           # The Ukrainian drinks tea.
                   'Green         == Ivory + 1',     # The green house is immediately to the right of the ivory house.
                   'OldGold       == Snails',        # The Old Gold smoker owns snails.
                   'Kools         == Yellow',        # Kools are smoked in the yellow house.
                   'Milk          == 3',             # Milk is drunk in the middle house.
                   'Norwegian     == 1',             # The Norwegian lives in the first house.
                   'abs(Chesterfields - Fox) == 1',  # The man who smokes Chesterfields lives in the house next to the man with the fox.
                   'abs(Kools - Horse) == 1',        # Kools are smoked in the house next to the house where the horse is kept.
                   'LuckyStrike   == OrangeJuice',   # The Lucky Strike smoker drinks orange juice.
                   'Japanese      == Parliaments',   # The Japanese smokes Parliaments.
                   'abs(Norwegian - Blue) == 1'      # The Norwegian lives next to the blue house.
                   } \
        | all_different(nations) \
        | all_different(drinks) \
        | all_different(pets) \
        | all_different(brands) \
        | all_different(colors)

    csp: CSP = (variables, values, constraints)
    solution: Assignment = solve2(csp)

    for x in solution:
        print(f'{x}: {solution[x]}')

    if solution is None:
        print('No solution found')
    else:
        _print_solution(solution, _Zebra(nations, drinks, pets, brands, colors))


if __name__ == '__main__':
    main()
