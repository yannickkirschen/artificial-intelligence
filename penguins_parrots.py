'''
Solve the following text problem using Z3.

(a) A Japanese deli offers both penguins and parrots.
(b) A parrot and a penguin together cost 666 bucks.
(c) The penguin costs 600 bucks more than the parrot.
(d) What is the price of the parrot?

You may assume that the prizes of these delicacies are integer valued.
'''

from z3 import Int, Solver, sat

penguin = Int('penguin')
parrot = Int('parrot')

s = Solver()
s.add(penguin + parrot == 666)
s.add(penguin - parrot == 600)

if s.check() == sat:
    m = s.model()
    print(f'The price of the parrot is {m[parrot]} bucks.')
