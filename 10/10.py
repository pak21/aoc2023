#!/usr/bin/env python3

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
            if c == 'S':
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
        case _: raise Exception(f"Couldn't determine start piece from signature {(right_back, up_back, left_back, down_back)}")

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
    return len([
        1
        for y in range(1, len(expanded_grid), 2)
        for x in range(1, len(expanded_grid[0]), 2)
        if expanded_grid[y][x] == '.' and (x, y) not in seen
    ])

with open(sys.argv[1]) as f:
    grid = [list(l.rstrip()) for l in f.readlines()]

start = find_start(grid)
grid[start[1]][start[0]] = start_type(grid, *start)

seen_p1 = part1(grid, start)

print(max(seen_p1.values()))

# We now want to ignore everything not in the main loop
grid_pipe_only = [
    [c if (x, y) in seen_p1 else '.' for x, c in enumerate(row)]
    for y, row
    in enumerate(grid)
]

expanded_grid = make_expanded_grid(grid_pipe_only)

print(part2(expanded_grid))

IS_CROSSING = {'|', '-', 'F', 'J'}

# Borrowing from a co-worker
#
# from a point, if you go diagonally, you can just count the letters that would
# create a "crossing" of the fence.  (i.e. if you travel up and to the left,
# you just need to count the number of | - F J you encounter until you get to
# the edge of the matrix

part2_2 = 0
last_crossings = [False] * len(grid_pipe_only[0])
for row in grid_pipe_only:
    new_crossings = [old ^ (c in IS_CROSSING) for c, old in zip(row, [False] + last_crossings)]
    part2_2 += len([1 for c, crossings in zip(row, new_crossings) if c == '.' and crossings])
    last_crossings = new_crossings

print(part2_2)
