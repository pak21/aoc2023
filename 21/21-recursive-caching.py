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
        return BASE_CACHE[cache_key]

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

def normalize_moves(grid, todo, max_moves, compute_fn):
    if not todo:
        return {}, [], [], [], []

    min_moves = todo[0][0]
    todo = [(n - min_moves, p) for n, p in todo]

    seen, r, u, l, d = compute_fn(grid, todo)

    seen = {moves + min_moves: plots for moves, plots in seen.items() if moves + min_moves <= max_moves}
    r = [(n + min_moves, p) for n, p in r if n + min_moves <= max_moves]
    u = [(n + min_moves, p) for n, p in u if n + min_moves <= max_moves]
    l = [(n + min_moves, p) for n, p in l if n + min_moves <= max_moves]
    d = [(n + min_moves, p) for n, p in d if n + min_moves <= max_moves]

    return seen, r, u, l, d

def base_puzzle(grid, todo, max_moves):
    return normalize_moves(grid, todo, max_moves, base_puzzle_)

SCALE_CACHE = {}

def split_to_subgrids(todo, subgrid_width, subgrid_height):
    subgrids = collections.defaultdict(list)
    for n, (x, y) in todo:
        grid_x = (x // subgrid_width)
        grid_y = (y // subgrid_height)
        subgrids[(grid_x, grid_y)].append((n, (x % subgrid_width, y % subgrid_height)))

    return subgrids
        
def min_x(scale, grid_x):
    n_grids = (3 ** scale) // 2
    return -n_grids * grid_x

def min_y(scale, grid_y):
    n_grids = (3 ** scale) // 2
    return -n_grids * grid_y

def scaled_(grid, todo, max_moves, scale):
    cache_key = (scale, tuple(todo))
    if cache_key in SCALE_CACHE:
        return SCALE_CACHE[cache_key]

    grid_width = (3 ** scale) * len(grid[0])
    grid_height = (3 ** scale) * len(grid)

    subgrid_width = (3 ** (scale - 1)) * len(grid[0])
    subgrid_height = (3 ** (scale - 1)) * len(grid)

    subgrids = split_to_subgrids(todo, subgrid_width, subgrid_height)
    grids_todo = list(subgrids.keys())
    grids_done = set()

    seen = collections.defaultdict(int)
    out_r = []
    out_u = []
    out_l = []
    out_d = []

    while len(grids_done) < 9:
        grid_pos = grids_todo.pop(0)
        if grid_pos in grids_done:
            continue

        grids_done.add(grid_pos)

        todo = sorted(subgrids[grid_pos])
        heapq.heapify(todo)

        if scale == 1:
            subgrid_seen, r, u, l, d = base_puzzle(grid, todo, max_moves)
        else:
            subgrid_seen, r, u, l, d = scaled(grid, todo, max_moves, scale - 1)

        for k, v in subgrid_seen.items():
            seen[k] += v

        grid_x, grid_y = grid_pos

        if grid_x == 2:
            r = [(n, (0, y + grid_y * subgrid_height)) for n, (x, y) in r]
            out_r += r
        else:
            r = [(n, (0, y)) for n, (x, y) in r]
            subgrids[(grid_x + 1, grid_y)] += r
            grids_todo.append((grid_x + 1, grid_y))

        if grid_y == 0:
            u = [(n, (x + grid_x * subgrid_width, grid_height - 1)) for n, (x, y) in u]
            out_u += u
        else:
            u = [(n, (x, subgrid_height - 1)) for n, (x, y) in u]
            subgrids[(grid_x, grid_y - 1)] += u
            grids_todo.append((grid_x, grid_y - 1))

        if grid_x == 0:
            l = [(n, (grid_width - 1, y + grid_y * subgrid_height)) for n, (x, y) in l]
            out_l += l
        else:
            l = [(n, (subgrid_width - 1, y)) for n, (x, y) in l]
            subgrids[(grid_x - 1, grid_y)] += l
            grids_todo.append((grid_x - 1, grid_y))

        if grid_y == 2:
            d = [(n, (x + grid_x * subgrid_width, 0)) for n, (x, y) in d]
            out_d += d
        else:
            d = [(n, (x, 0)) for n, (x, y) in d]
            subgrids[(grid_x, grid_y + 1)] += d
            grids_todo.append((grid_x, grid_y + 1))

    SCALE_CACHE[cache_key] = (seen, out_r, out_u, out_l, out_d)

    return seen, out_r, out_u, out_l, out_d

def scaled(grid, todo, max_moves, scale):
    return normalize_moves(grid, todo, max_moves, lambda g, t: scaled_(g, t, max_moves, scale))

def main():
    grid, start = parse(sys.argv[1])
    max_moves = int(sys.argv[2])
    scale = int(sys.argv[3])

    start = (start[0] - min_x(scale, len(grid[0])), start[1] - min_y(scale, len(grid)))

    todo = [(0, start)]
    if scale == 0:
        seen, r, u, l, d = base_puzzle(grid, todo, max_moves)
    else:
        seen, r, u, l, d = scaled(grid, todo, max_moves, scale)

    print(sum(plots for moves, plots in seen.items() if moves <= max_moves and moves % 2 == max_moves % 2))

if __name__ == '__main__':
    main()
