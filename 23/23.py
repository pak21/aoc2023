#!/usr/bin/env python3

import heapq
import sys

def can_move(pos, trails):
    x, y = pos

    if y < 0 or y >= len(trails):
        return False

    return trails[y][x] != '#'
    
def next_positions_part1(pos, trails):
    x, y = pos
    match trails[y][x]:
        case '.': return [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1) ]
        case '>': return [(x + 1, y)]
        case 'v': return [(x, y + 1)]

def next_positions_part2(pos, trails):
    x, y = pos
    return [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1) ]

def walk(trails, start, poi, next_pos_fn):
    todo = [(start, set())]

    edges = {}
    while todo:
        pos, seen = todo.pop(0)

        for next_pos in next_pos_fn(pos, trails):
            if can_move(next_pos, trails) and next_pos not in seen:
                if next_pos in poi:
                    edges[next_pos] = len(seen) + 1
                else:
                    todo.append((next_pos, seen | {pos}))

    return edges

def find_junctions(trails):
    for y in range(1, len(trails)-1):
        row = trails[y]
        for x in range(1, len(row)-1):
            if trails[y][x] != '#':
                right = trails[y][x+1] != '#'
                up = trails[y-1][x] != '#'
                left = trails[y][x-1] != '#'
                down = trails[y+1][x] != '#'

                moves = right + up + left + down

                if moves > 2:
                    yield (x, y)

def walk_graph(graph, start, end):
    todo = [(0, start, set())]

    longest = 0
    while todo:
        moves, pos, seen = heapq.heappop(todo)

        for next_pos, moves_to_next in graph[pos].items():
            if next_pos not in seen:
                next_moves = moves - moves_to_next
                if next_pos == end:
                    if next_moves < longest:
                        longest = next_moves
                else:
                    heapq.heappush(todo, (next_moves, next_pos, seen | {pos}))

    return -longest

def do_part(trails, start, end, poi, next_pos_fn):
    graph = {start: walk(trails, start, poi, next_pos_fn) for start in poi}
    return walk_graph(graph, start, end)

def main():
    with open(sys.argv[1]) as f:
        trails = [list(r.rstrip()) for r in f]

    start = (1, 0)
    end = (len(trails[0]) - 2, len(trails) - 1)

    poi = [start, end] + list(find_junctions(trails))

    for next_pos_fn in [next_positions_part1, next_positions_part2]:
        print(do_part(trails, start, end, poi, next_pos_fn))

if __name__ == '__main__':
    main()
