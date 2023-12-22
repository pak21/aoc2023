#!/usr/bin/env python3

import sys

def parse(fn):
    with open(fn) as f:
        grid = [list(r.rstrip()) for r in f]

    for y, r in enumerate(grid):
        for x, c in enumerate(r):
            if c == 'S':
                start = (x, y)

    grid = [[c == '#' for c in r] for r in grid]

    return (grid, start)

def next_points(p):
    yield (p[0] + 1, p[1])
    yield (p[0], p[1] - 1)
    yield (p[0] - 1, p[1])
    yield (p[0], p[1] + 1)

def part1(grid, start, max_n):
    seen = set()
    result = 0

    todo = [(0, start)]
    while todo:
        n, p = todo.pop(0)

        if n > max_n:
            break

        if p in seen:
            continue

        seen.add(p)
        if n % 2 == max_n % 2:
            result += 1

        for np in next_points(p):
            if not grid[np[1] % len(grid)][np[0] % len(grid[0])]:
                todo.append((n + 1, np))
                
    return result

def main():
    grid, start = parse(sys.argv[1])

    results = [part1(grid, start, 65 + n * 131) for n in range(3)]

    # f(x) = ax^2 + bx + c
    # => f(0) =           c
    #    f(1) =  a +  b + c
    #    f(2) = 4a + 2b + c
    #
    # p = f(1) - f(0) =  a + b
    # q = f(2) - f(1) = 3a + b
    # => q - p = 2a
    # => a = 1/2 (f(2) - 2f(1) + f(0))

    a = (results[2] - 2 * results[1] + results[0]) // 2
    b = results[1] - results[0] - a
    c = results[0]

    x = (26501365 - 65) // 131

    print(a*x**2 + b*x + c)

if __name__ == '__main__':
    main()
