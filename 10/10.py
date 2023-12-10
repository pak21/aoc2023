#!/usr/bin/env python3

import operator
import sys

CONNECTIONS = {
    '-': [(1, 0), (-1, 0)],
    '|': [(0, -1), (0, 1)],
    '7': [(-1, 0), (0, 1)],
    'F': [(1, 0), (0, 1)],
    'J': [(0, -1), (-1, 0)],
    'L': [(1, 0), (0, -1)],

    '.': []
}

def find_start(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if grid[y][x] == 'S':
                return (x, y)

    raise Exception('Start not found')

def start_type(grid, x, y):
    right_back = (-1, 0) in CONNECTIONS[grid[y][x+1]]
    up_back = (0, 1) in CONNECTIONS[grid[y-1][x]]
    left_back = (1, 0) in CONNECTIONS[grid[y][x-1]]
    down_back = (0, -1) in CONNECTIONS[grid[y+1][x]]

    match (right_back, up_back, left_back, down_back):
        case (False, False, True, True): return '7'
        case (False, True, False, True): return '|'
        case (False, True, True, False): return 'J'
        case (True, False, False, True): return 'F'
        case (True, False, True, False): return '-'
        case (True, True, False, False): return 'L'
        case _: raise Exception((right_back, up_back, left_back, down_back))

def part1(grid, start):
    todo = [(start, 0)]
    seen = {}

    while todo:
        (x, y), moves = todo.pop(0)
        if (x, y) in seen:
            continue

        seen[(x, y)] = moves

        for dx, dy in CONNECTIONS[grid[y][x]]:
            todo.append(((x+dx, y+dy), moves+1))

    return seen

def make_expanded_grid(grid_pipe_only):
    # Expand the grid to twice the size, filling in the connector pieces
    # This deliberately adds a border of '.' round the whole thing so we don't have to deal with
    # the literal edge case of pipes being up against the current border
    height2 = 2 * len(grid_pipe_only) + 1
    width2 = 2 * len(grid_pipe_only[0]) + 1
    grid2 = [['.'] * width2 for _ in range(height2)]

    for y, row in enumerate(grid_pipe_only):
        for x, c in enumerate(row):
            ny = 2*y+1
            nx = 2*x+1
            grid2[ny][nx] = c

            for dx, dy in CONNECTIONS[c]:
                grid2[ny+dy][nx+dx] = '#'

    return grid2

def part2(expanded_grid):
    # Find everything connected to the outside on the bigger grid
    todo = [(0, 0)]
    seen = set()

    while todo:
        (x, y) = todo.pop(0)

        if (x, y) in seen or x < 0 or x >= len(expanded_grid[0]) or y < 0 or y >= len(expanded_grid):
            continue

        seen.add((x, y))

        if expanded_grid[y][x] == '.':
            todo.append((x+1, y))
            todo.append((x, y-1))
            todo.append((x-1, y))
            todo.append((x, y+1))

    # And count empty spaces _from the original grid_ which we couldn't visit
    return sum([
        expanded_grid[y][x] == '.' and (x, y) not in seen
        for y in range(1, len(expanded_grid), 2)
        for x in range(1, len(expanded_grid[0]), 2)
    ])

with open(sys.argv[1]) as f:
    grid = [list(l.rstrip()) for l in f.readlines()]

start = find_start(grid)
grid[start[1]][start[0]] = start_type(grid, *start)

seen_p1 = part1(grid, start)

print(sorted(seen_p1.items(), key=operator.itemgetter(1))[-1][1])

# We now want to ignore everything not in the main loop
grid_pipe_only = [
    [c if (x, y) in seen_p1 else '.' for x, c in enumerate(grid[y])]
    for y
    in range(len(grid))
]

expanded_grid = make_expanded_grid(grid_pipe_only)

print(part2(expanded_grid))
