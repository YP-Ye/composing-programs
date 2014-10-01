def absolute_value(x):
    """
    Poor Pythonista's ternary ?: operator.  (When does this not match ?:
    semantics?)

    >>> absolute_value(-2)
    2
    >>> absolute_value(0)
    0
    >>> absolute_value(-2)
    2
    """
    return x > 0 and x or -x

if __name__ == '__main__':
    from doctest import testmod
    print(testmod())
