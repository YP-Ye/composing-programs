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
