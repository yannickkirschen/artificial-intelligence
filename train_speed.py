'''
Solve the following text problem using Z3.

(a) A train travels at a uniform speed for 360 miles.
(b) The train would have taken 48 minutes less to travel the same distance if it had been faster by 5 miles per hour.

Find the speed of the train!

Hints:
1. As the speed is a real number you should declare this variable via the Z3 function Real instead of using the function Int.
2. 48 minutes are four fifth of an hour. The fraction 4/5 can be represented in Z3 by the expression Q(4, 5).
3. When you formulate the information given above, you will get a system of non-linear equations, which is equivalent to
   a quadratic equation. This quadratic equation has two different solutions. One of these solutions is negative. In
   order to exclude the negative solution you need to add a constraint stating that the speed of the train has to be
   greater than zero.
4. The solution will be some real number which is represented internally as an object of type RatNumRef. If o is an
   object of this type, then this object can be converted to a string as follows: o.as_decimal(17)
   Here, 17 is the number of digits following the decimal point. This string can be then converted
   to a float by using the function float().
'''

from z3 import Real, Q, Solver, sat


velocity = Real('velocity')
time = Real('time')

s = Solver()
s.add(velocity * time == 360)
s.add((velocity + 5) * (time - Q(4, 5)) == 360)
s.add(velocity >= 0)

if s.check() == sat:
    m = s.model()
    print(f'The velocity of the train is {m[velocity]} miles per hour.')
