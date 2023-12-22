#!/usr/bin/env python3

import enum
import heapq
import sys

def parse(fn):
    with open(fn) as f:
        grid = [list(r.rstrip()) for r in f]

    grid = [[c == '#' for c in r] for r in grid]

    start = (len(grid[0]) // 2, len(grid) // 2)

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
    
def part1(grid, todo, max_moves):
    seen = {}
    right = []
    up = []
    left = []
    down = []

    while todo:
        n, p = heapq.heappop(todo)

        if n > max_moves:
            break

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
                
    return seen, right, up, left, down

def part1_with_min(grid, todo, max_moves):
    min_moves = todo[0][0]
    corrected = [(n - min_moves, p) for n, p in todo]
    seen, right, up, left, down = part1(grid, corrected, max_moves)

    seen = {p: n + min_moves for p, n in seen.items()}
    right = [(n + min_moves, p) for n, p in right]
    up = [(n + min_moves, p) for n, p in up]
    left = [(n + min_moves, p) for n, p in left]
    down = [(n + min_moves, p) for n, p in down]

    return seen, right, up, left, down

def main():
    grid, start = parse(sys.argv[1])
    max_n = int(sys.argv[2])

    seen, r, u, _, _ = part1_with_min(grid, [(0, start)], max_n)

    print(len([1 for n in seen.values() if n <= max_n and n % 2 == max_n % 2]))

if __name__ == '__main__':
    main()
