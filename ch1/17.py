def count_partitions_DP(n, m):
    """Count the ways to partition n using parts up to m.

    We use a technique known as "dynamic programming" (DP), which sounds more
    magical than it is: essentially, we compute intermediate results and store
    them in a table.  It's really just recursion plus caching, minus the
    recursive function calls.

    >>> count_partitions_DP(6, 4)
    9
    >>> count_partitions_DP(5, 5)
    7
    >>> count_partitions_DP(10, 10)
    42
    >>> count_partitions_DP(15, 15)
    176
    >>> count_partitions_DP(20, 20)
    627
    """
    # T[i][j] is the number of partitions of i into parts of size j or less.
    T = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        T[i][0] = 0
    for j in range(m + 1):
        T[0][j] = 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            T[i][j] = T[i][j - 1]
            if i >= j:
                T[i][j] += T[i - j][j]
    return T[n][m]

if __name__ == '__main__':
    from doctest import testmod
    print(testmod())
