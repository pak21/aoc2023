#!/usr/bin/env python3

import operator
import sys

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
        case ('J', '.', '7', '|'): return 'F'
        case ('|', 'F', 'L', '7'): return 'J'
        case ('7', 'L', 'J', 'J'): return 'F'
        case ('F', 'J', 'F', '|'): return '7'
        case _: raise Exception(f"Can't match start with {(right, up, left, down)}")

with open(sys.argv[1]) as f:
    grid = [list(l.rstrip()) for l in f.readlines()]

start = find_start(grid)
repl = start_type(grid, start)
grid[start[1]][start[0]] = repl

todo = [(start, 0)]
seen = {}

while todo:
    (x, y), moves = todo.pop(0)
    if (x, y) in seen:
        continue

    seen[(x, y)] = moves

    match grid[y][x]:
        case 'F':
            todo.append(((x+1, y), moves+1))
            todo.append(((x, y+1), moves+1))
        case '-':
            todo.append(((x+1, y), moves+1))
            todo.append(((x-1, y), moves+1))
        case '|':
            todo.append(((x, y+1), moves+1))
            todo.append(((x, y-1), moves+1))
        case '7':
            todo.append(((x-1, y), moves+1))
            todo.append(((x, y+1), moves+1))
        case 'L':
            todo.append(((x+1, y), moves+1))
            todo.append(((x, y-1), moves+1))
        case 'J':
            todo.append(((x-1, y), moves+1))
            todo.append(((x, y-1), moves+1))
        case _:
            raise Exception(f'Unknown symbol {grid[y][x]} at {(x, y)}')

furthest = sorted(seen.items(), key=operator.itemgetter(1))[-1][1]
print(furthest)

for y in range(len(grid)):
    for x in range(len(grid[0])):
        if (x, y) not in seen:
            grid[y][x] = '.'

w = len(grid[0])
w2 = 2 * w + 1
grid2 = [['.'] * w2]
for row in grid:
    grid2.append(['.'] * w2)
    grid2.append(['.'] * w2)

for y, row in enumerate(grid):
    for x, c in enumerate(row):
        ny = 2*y+1
        nx = 2*x+1
        grid2[ny][nx] = c

        match c:
            case 'F':
                grid2[ny+1][nx] = '|'
                grid2[ny][nx+1] = '-'
            case '-':
                grid2[ny][nx-1] = '-'
                grid2[ny][nx+1] = '-'
            case '7':
                grid2[ny+1][nx] = '|'
                grid2[ny][nx-1] = '-'
            case '|':
                grid2[ny+1][nx] = '|'
                grid2[ny-1][nx] = '|'
            case 'L':
                grid2[ny-1][nx] = '|'
                grid2[ny][nx+1] = '-'
            case 'J':
                grid2[ny-1][nx] = '|'
                grid2[ny][nx-1] = '-'
            case '.': pass
            case _: raise Exception(c)

todo = [(0, 0)]
seen = set()

while todo:
    (x, y) = todo.pop(0)

    if (x, y) in seen:
        continue

    if x < 0 or x >= len(grid2[0]) or y < 0 or y >= len(grid2):
        continue

    seen.add((x, y))

    match grid2[y][x]:
        case '.':
            todo.append((x+1, y))
            todo.append((x, y-1))
            todo.append((x-1, y))
            todo.append((x, y+1))
        case _: pass

n = 0
for y in range(1, len(grid2), 2):
    for x in range(1, len(grid2[0]), 2):
        if grid2[y][x] == '.' and (x, y) not in seen:
            n += 1

print(n)
