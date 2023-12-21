#!/usr/bin/env python3

import collections
import enum
import heapq
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

class Action(enum.Enum):
    MOVE = enum.auto(),
    BLOCKED = enum.auto(),

    OFF_RIGHT = enum.auto(),
    OFF_UP = enum.auto(),
    OFF_LEFT = enum.auto(),
    OFF_DOWN = enum.auto(),
 
def can_move(p, grid):
    if p[0] < 0:
        return Action.OFF_LEFT

    if p[0] >= len(grid[0]):
        return Action.OFF_RIGHT

    if p[1] < 0:
        return Action.OFF_UP

    if p[1] >= len(grid):
        return Action.OFF_DOWN

    return Action.BLOCKED if grid[p[1]][p[0]] else Action.MOVE
    
BASE_CACHE = {}

def base_puzzle_(grid, todo):
    cache_key = tuple(todo)
    if cache_key in BASE_CACHE:
        seen, right, up, left, down = BASE_CACHE[cache_key]
        return seen, right, up, left, down

    print('  not cached')

    seen = {}
    right = []
    up = []
    left = []
    down = []

    while todo:
        n, p = heapq.heappop(todo)

        if p in seen:
            continue

        seen[p] = n

        for np in next_points(p):
            action = can_move(np, grid)
            match action:
                case Action.MOVE: heapq.heappush(todo, (n + 1, np))
                case Action.BLOCKED: pass
                case Action.OFF_RIGHT: heapq.heappush(right, (n + 1, np))
                case Action.OFF_UP: heapq.heappush(up, (n + 1, np))
                case Action.OFF_LEFT: heapq.heappush(left, (n + 1, np))
                case Action.OFF_DOWN: heapq.heappush(down, (n + 1, np))

    seen = collections.Counter(seen.values())

    BASE_CACHE[cache_key] = (seen, right, up, left, down)
    
    return seen, right, up, left, down

def base_puzzle(grid, todo):
    min_moves = todo[0][0]
    todo = [(n - min_moves, p) for n, p in todo]

    seen, r, u, l, d = base_puzzle_(grid, todo)

    seen = {moves + min_moves: plots for moves, plots in seen.items()}
    r = [(n + min_moves, p) for n, p in r]
    u = [(n + min_moves, p) for n, p in u]
    l = [(n + min_moves, p) for n, p in l]
    d = [(n + min_moves, p) for n, p in d]

    return seen, r, u, l, d

def main():
    grid, start = parse(sys.argv[1])
    max_moves = int(sys.argv[2])

    grid_moves = collections.defaultdict(list)
    grid_moves[(0, 0)] = [(0, start)]
    grids_todo = [(0, 0)]
    grids_done = set()

    while grids_todo:
        grid_x, grid_y = grids_todo.pop(0)
        if (grid_x, grid_y) in grids_done:
            continue

        if grid_x == 4:
            break

        grids_done.add((grid_x, grid_y))

        todo = grid_moves[(grid_x, grid_y)]
        heapq.heapify(todo)

        print(grid_x, grid_y)
        seen, r, u, l, d = base_puzzle(grid, todo)

        r = [(n, (x - len(grid[0]), y)) for n, (x, y) in r]
        grid_moves[(grid_x + 1, grid_y)] += r
        grids_todo.append((grid_x + 1, grid_y))

        u = [(n, (x, y + len(grid))) for n, (x, y) in u]
        grid_moves[(grid_x, grid_y - 1)] += u
        grids_todo.append((grid_x, grid_y - 1))

        l = [(n, (x + len(grid[0]), y)) for n, (x, y) in l]
        grid_moves[(grid_x - 1, grid_y)] += l
        grids_todo.append((grid_x - 1, grid_y))

        d = [(n, (x, y - len(grid))) for n, (x, y) in d]
        grid_moves[(grid_x, grid_y + 1)] += d
        grids_todo.append((grid_x, grid_y + 1))

if __name__ == '__main__':
    main()
