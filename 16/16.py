#!/usr/bin/env python3

import sys

puzzle = {}

with open(sys.argv[1]) as f:
    for y, row in enumerate(f):
        for x, c in enumerate(row):
            puzzle[(x, y)] = c

max_x = x
max_y = y+1

def part1(initial):
    seen = set()
    todo = [initial]

    while todo:
        (old_x, old_y), direction = todo.pop(0)
        if ((old_x, old_y), direction) in seen:
            continue

        seen.add(((old_x, old_y), direction))

        new_beams = []
        cell = puzzle.get((old_x, old_y))

        match (cell, direction):
            case ('.', 0): new_beams.append(((old_x + 1, old_y), 0))
            case ('.', 1): new_beams.append(((old_x, old_y - 1), 1))
            case ('.', 2): new_beams.append(((old_x - 1, old_y), 2))
            case ('.', 3): new_beams.append(((old_x, old_y + 1), 3))

            case ('/', 0): new_beams.append(((old_x, old_y - 1), 1))
            case ('/', 1): new_beams.append(((old_x + 1, old_y), 0))
            case ('/', 2): new_beams.append(((old_x, old_y + 1), 3))
            case ('/', 3): new_beams.append(((old_x - 1, old_y), 2))

            case ('\\', 0): new_beams.append(((old_x, old_y + 1), 3))
            case ('\\', 1): new_beams.append(((old_x - 1, old_y), 2))
            case ('\\', 2): new_beams.append(((old_x, old_y - 1), 1))
            case ('\\', 3): new_beams.append(((old_x + 1, old_y), 0))

            case ('|', 0):
                new_beams.append(((old_x, old_y - 1), 1))
                new_beams.append(((old_x, old_y + 1), 3))
            case ('|', 1): new_beams.append(((old_x, old_y - 1), 1))
            case ('|', 2):
                new_beams.append(((old_x, old_y - 1), 1))
                new_beams.append(((old_x, old_y + 1), 3))
            case ('|', 3): new_beams.append(((old_x, old_y + 1), 3))

            case ('-', 0): new_beams.append(((old_x + 1, old_y), 0))
            case ('-', 1):
                new_beams.append(((old_x + 1, old_y), 0))
                new_beams.append(((old_x - 1, old_y), 2))
            case ('-', 2): new_beams.append(((old_x - 1, old_y), 2))
            case ('-', 3):
                new_beams.append(((old_x + 1, old_y), 0))
                new_beams.append(((old_x - 1, old_y), 2))

            case _: raise Exception(cell, direction)

        for (new_x, new_y), new_dir in new_beams:
            if new_x >= 0 and new_x < max_x and new_y >= 0 and new_y < max_y:
                todo.append(((new_x, new_y), new_dir))

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
