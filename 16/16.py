#!/usr/bin/env python3

import collections
import sys

puzzle = {}

with open(sys.argv[1]) as f:
    puzzle = [l.rstrip() for l in f]

max_x = len(puzzle[0])
max_y = len(puzzle)

def next_beam(old_x, old_y, direction):
    match direction:
        case 0: return (old_x+1, old_y)
        case 1: return (old_x, old_y-1)
        case 2: return (old_x-1, old_y)
        case 3: return (old_x, old_y+1)

def part1(initial):
    seen = set()
    todo = collections.deque([initial])

    while todo:
        (old_x, old_y), direction = todo.popleft()

        if ((old_x, old_y), direction) in seen or old_x < 0 or old_x >= max_x or old_y < 0 or old_y >= max_y:
            continue

        seen.add(((old_x, old_y), direction))

        new_dirs = []
        match (puzzle[old_y][old_x], direction):
            case ('.', _): new_dirs = [direction]

            case ('/', 0): new_dirs = [1]
            case ('/', 1): new_dirs = [0]
            case ('/', 2): new_dirs = [3]
            case ('/', 3): new_dirs = [2]

            case ('\\', 0): new_dirs = [3]
            case ('\\', 1): new_dirs = [2]
            case ('\\', 2): new_dirs = [1]
            case ('\\', 3): new_dirs = [0]

            case ('|', _) if direction % 2 == 0: new_dirs = [1, 3]
            case ('|', _) if direction % 2 == 1: new_dirs = [direction]

            case ('-', _) if direction % 2 == 0: new_dirs = [direction]
            case ('-', _) if direction % 2 == 1: new_dirs = [0, 2]

        todo += [(next_beam(old_x, old_y, nd), nd) for nd in new_dirs]

    return len(set([s[0] for s in seen]))

print(part1(((0, 0), 0)))

part2 = 0
for y in range(max_y):
    from_left = part1(((0, y), 0))
    from_right = part1(((max_x - 1, y), 2))
    part2 = max(part2, from_left, from_right)

for x in range(max_x):
    from_top = part1(((x, 0), 3))
    from_bottom = part1(((x, max_y - 1), 1))
    part2 = max(part2, from_top, from_bottom)

print(part2)
