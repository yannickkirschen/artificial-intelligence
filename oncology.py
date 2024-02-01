'''
In an oncology ward, five patients are lying in adjacent rooms. Except for one of the patients, each has smoked exactly
one brand of cigarette. The patient who did not smoke cigarettes smoked a pipe. Each patient drives exactly one car and
is diagnosed with exactly one type of cancer. Additionally, we have the following information:

1. In the room next to Michael, Camel is being smoked.
2. The Trabant driver smokes Harvest 23 and is in the room next to the tongue cancer patient.
3. Rolf is in the last room and has laryngeal cancer.
4. The West smoker is in the first room.
5. The Mazda driver has tongue cancer and is next to the Trabant driver.
6. The Nissan driver is next to the tongue cancer patient.
7. Rudolf is desperately begging for euthanasia and his room is between the room of the Camel smoker and the room of the Trabant driver.
8. Tomorrow is the last birthday of the Seat driver.
9. The Luckies smoker is next to the patient with lung cancer.
10. The Camel smoker is next to the patient with intestinal cancer.
11. The Nissan driver is next to the Mazda driver.
12. The Mercedes driver smokes a pipe and is next to the Camel smoker.
13. Jens is next to the Luckies smoker.
14. Yesterday, the patient with testicular cancer flushed his balls down the toilet.

Given this information, the task is to answer the following questions:
    1. What does the intestinal cancer patient smoke?
    2. What car does Kurt drive?

Your task is to formulate this puzzle as a constraint satisfaction problem.
'''

from dataclasses import dataclass

from tabulate import tabulate

from backtrack_solver import CSP, Solution, all_different, solve


@dataclass
class _Oncology:
    names: set[str]
    brands: set[str]
    cars: set[str]
    cancers: set[str]


def _print_solution(solution: Solution, data: _Oncology) -> None:
    rooms: list[list[str]] = []

    for i in range(1, 5+1):
        room: list[str] = [f'{i}']
        for _class in [data.names, data.brands, data.cars, data.cancers]:
            for x in _class:
                if solution[x] == i:
                    room.append(x)
        rooms.append(room)

    print(tabulate(rooms, headers=['Room', 'Name', 'Brand', 'Car', 'Cancer'], tablefmt='pretty'))
    print()

    for room in rooms:
        if room[1] == 'Kurt':
            print(f'Kurt drives a {room[3]}')
        if room[4] == 'intestinal':
            print(f'The intestinal cancer patient smokes {room[2]}')


def main():
    '''Main function for the oncology puzzle.'''

    names = {'Michael', 'Rolf', 'Rudolf', 'Jens', 'Kurt'}
    brands = {'Camel', 'Harvest', 'West', 'Luckies', 'Pipe'}
    cars = {'Trabant', 'Mazda', 'Nissan', 'Seat', 'Mercedes'}
    cancers = {'lung', 'tongue', 'laryngeal', 'intestinal', 'testicular'}

    variables = names | brands | cars | cancers
    values = {1, 2, 3, 4, 5}
    constraints = {
        # In the room next to Michael, Camel is being smoked.
        'abs(Michael - Camel) == 1',

        # The Trabant driver smokes Harvest 23 and is in the room next to the tongue cancer patient.
        'Trabant == Harvest',
        'abs(Trabant - tongue) == 1',
        'abs(Harvest - tongue) == 1',

        # Rolf is in the last room and has laryngeal cancer.
        'Rolf == 5 and Rolf == laryngeal',

        # The West smoker is in the first room.
        'West == 1',

        # The Mazda driver has tongue cancer and is next to the Trabant driver.
        'Mazda == tongue',
        'abs(Mazda - Trabant) == 1',
        'abs(tongue - Trabant) == 1',

        # The Nissan driver is next to the tongue cancer patient.
        'abs(Nissan - tongue) == 1',

        # Rudolf is desperately begging for euthanasia and his room is between the room of the Camel smoker
        # and the room of the Trabant driver.
        'Rudolf - Camel + 2 == Trabant or Rudolf - Trabant + 2 == Camel',

        # '',  # Tomorrow is the last birthday of the Seat driver.

        # The Luckies smoker is next to the patient with lung cancer.
        'abs(Luckies - lung) == 1',

        # The Camel smoker is next to the patient with intestinal cancer.
        'abs(Camel - intestinal) == 1',

        # The Nissan driver is next to the Mazda driver.
        'abs(Nissan - Mazda) == 1',

        # The Mercedes driver smokes a pipe and is next to the Camel smoker.
        'Mercedes == Pipe',
        'abs(Mercedes - Camel) == 1',
        'abs(Pipe - Camel) == 1',

        # Jens is next to the Luckies smoker.
        'abs(Jens - Luckies) == 1',

        # ''  # Yesterday, the patient with testicular cancer flushed his balls down the toilet.
    } \
        | all_different(names)\
        | all_different(brands) \
        | all_different(cars)\
        | all_different(cancers)

    csp: CSP = (variables, values, constraints)
    solution: Solution = solve(csp)

    if solution is None:
        print('No solution found')
    else:
        _print_solution(solution, _Oncology(names, brands, cars, cancers))


if __name__ == '__main__':
    main()
