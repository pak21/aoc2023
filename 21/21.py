#!/usr/bin/env python3

import sys

def parse(fn):
    with open(fn) as f:
        grid = f.readlines()

    grid_width = len(grid[0]) - 1
    grid_height = len(grid)

    grid = {(x, y) for y, r in enumerate(grid) for x, c in enumerate(r.rstrip()) if c == '#'}

    return grid, grid_width, grid_height

def next_points(p):
    yield (p[0] + 1, p[1])
    yield (p[0], p[1] - 1)
    yield (p[0] - 1, p[1])
    yield (p[0], p[1] + 1)

def can_move(p, grid, grid_width, grid_height):
    if p[0] < 0 or p[0] >= grid_width or p[1] < 0 or p[1] >= grid_height:
        return False

    return not p in grid
    
def part1(grid, grid_width, grid_height, start, max_moves):
    todo = [(0, start)]
    seen = set()
    result = 0

    while todo:
        n, p = todo.pop(0)

        if n > max_moves:
            break

        if p in seen:
            continue

        seen.add(p)

        if n % 2 == max_moves % 2:
            result += 1

        for np in next_points(p):
            if can_move(np, grid, grid_width, grid_height):
                todo.append((n + 1, np))
                
    return result

def main():
    grid, grid_width, grid_height = parse(sys.argv[1])
    max_n = int(sys.argv[2])

    print(part1(grid, grid_width, grid_height, (grid_width // 2, grid_height // 2), max_n))

if __name__ == '__main__':
    main()
