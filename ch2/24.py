import random
import time
import sys

d = {}
# NOTE: this doesn't work either - the entire value must
# be hashable!
#d[(1, [])] = 2

class HashBomb(object):
    def __init__(self, x):
        self._x = x
    def get(self):
        return self._x
    def __cmp__(self, other):
        return self._x - other._x
    def __eq__(self, other):
        return self._x == other._x
    def __hash__(self):
        # NOTE: we deliberately introduce poor hashing behavior to demonstrate
        # the "bucket-linear" time of Python dict operations.
        return 42

try:
    n = int(sys.argv[1])
except (IndexError, ValueError):
    n = 100

for i in range(n):
    x = HashBomb(i)
    d[x] = i

start = time.time()
t, m = 0, 1000
for i in range(m):
    j = random.randrange(n)
    t += d[HashBomb(j)]
elapsed = time.time() - start
print('Finished %d iterations on size %d in %.3fs' % (m, n, elapsed))

def add3(x):
    def add2(x):
        y = x
        def add1(z):
            nonlocal x
            nonlocal y
            return x + y + z
        return add1
    return add2

# NOTE: this prints 8 and not 9, as the outermost x (in add3) is obscured
# by the middle x (in add2).  There is no such problem with y, which is not
# obscured by an intermediate scope.
print(add3(4)(3)(2))

from operator import add, sub, mul, truediv
import math

def connector(name = None):
    """A connector between constraints."""
    informant = None
    constraints = []
    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints)
        else:
            if val != value:
                print('Contradiction detected:', val, 'vs', value)
    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    connector = {'val': None,
                 'set_val': set_value,
                 'forget': forget_value,
                 'has_val': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}
    return connector

def inform_all_except(source, message, constraints):
    """Inform all constraints of the message, except source."""
    for c in constraints:
        if c != source:
            c[message]()

def make_ternary_constraint(a, b, c, ab, ca, cb):
    """Constraint:

    ab(a, b) == c
    ca(c, a) == b
    cb(c, b) == a"""
    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))
    def forget_value():
        for connector in (a, b, c):
            connector['forget'](constraint)
    constraint = {'new_val': new_value, 'forget': forget_value}
    for connector in (a, b, c):
        connector['connect'](constraint)
    return constraint

def adder(a, b, c):
    """Constraint:

    a + b == c"""
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    """Constraint:

    a * b == c"""
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def power(a, b, c):
    """Constraint:

    a ** b == c"""
    return make_ternary_constraint(
        a, b, c,
        math.pow,
        math.log,
        lambda c, b: math.pow(c, 1 / b))

def constant(connector, value):
    """Constraint:

    connector == value"""
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

final_value = connector('Final Value')
initial_value = connector('Initial Value')
interest_rate = connector('Interest Rate')
time_elapsed = connector('Time Elapsed')

def interest_calculator(b, a, r, t):
    u = connector()
    v = connector()
    w = connector()
    adder(w, r, u)
    power(u, t, v)
    multiplier(v, a, b)
    constant(w, 1)

interest_calculator(final_value, initial_value, interest_rate, time_elapsed)

initial_value['set_val']('user', 1000)
interest_rate['set_val']('user', 0.05)
time_elapsed['set_val']('user', 10)

final_value['set_val']('user', 10000)

time_elapsed['forget']('user')
final_value['set_val']('user', 10000)
