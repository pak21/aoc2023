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

def start_type(grid, start):
    (x, y) = start
    right = grid[y][x+1]
    up = grid[y-1][x]
    left = grid[y][x-1]
    down = grid[y+1][x]

    match (right, up, left, down):
        case ('-', '.', '.', '|'): return 'F'
        case ('|', 'F', 'L', '7'): return 'J'
        case ('7', 'L', 'J', 'J'): return 'F'
        case ('F', 'J', 'F', '|'): return '7'
        case ('J', '.', '7', '|'): return 'F'
        case _: raise Exception(f"Can't match start with {(right, up, left, down)}")

with open(sys.argv[1]) as f:
    grid = [list(l.rstrip()) for l in f.readlines()]

start = find_start(grid)
grid[start[1]][start[0]] = start_type(grid, start)

todo = [(start, 0)]
seen = {}

while todo:
    (x, y), moves = todo.pop(0)
    if (x, y) in seen:
        continue

    seen[(x, y)] = moves

    for dx, dy in CONNECTIONS[grid[y][x]]:
        todo.append(((x+dx, y+dy), moves+1))

print(sorted(seen.items(), key=operator.itemgetter(1))[-1][1])

# We now want to ignore everything not in the main loop
for y in range(len(grid)):
    grid[y] = [c if (x, y) in seen else '.' for x, c in enumerate(grid[y])]

# Expand the grid to twice the size, filling in the connector pieces
# This deliberately adds a border of '.' round the whole thing so we don't have to deal with
# the literal edge case of pipes being up against the current border
w2 = 2 * len(grid[0]) + 1
grid2 = [['.'] * w2]
for row in grid:
    grid2.append(['.'] * w2)
    grid2.append(['.'] * w2)

for y, row in enumerate(grid):
    for x, c in enumerate(row):
        ny = 2*y+1
        nx = 2*x+1
        grid2[ny][nx] = c

        for dx, dy in CONNECTIONS[c]:
            grid2[ny+dy][nx+dx] = '#'

# Find everything connected to the outside on the bigger grid
todo = [(0, 0)]
seen = set()

while todo:
    (x, y) = todo.pop(0)

    if (x, y) in seen or x < 0 or x >= len(grid2[0]) or y < 0 or y >= len(grid2):
        continue

    seen.add((x, y))

    match grid2[y][x]:
        case '.':
            todo.append((x+1, y))
            todo.append((x, y-1))
            todo.append((x-1, y))
            todo.append((x, y+1))
        case _: pass

# And count empty spaces _from the original grid_ which we couldn't visit
print(sum([grid2[y][x] == '.' and (x, y) not in seen for y in range(1, len(grid2), 2) for x in range(1, len(grid2[0]), 2)]))
