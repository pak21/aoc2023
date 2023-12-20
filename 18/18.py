#!/usr/bin/env python3

import collections
import re
import sys

DIRS = {
    'R': (1, 0),
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1)
}

PART2_LOOKUP = ['R', 'D', 'L', 'U']

def parse_line(l, part):
    match = re.match(r'^(.) (\d+) \(#([0-9a-f]{5})(\d)\)$', l)
    match part:
        case 1: return match.group(1), int(match.group(2))
        case 2: return PART2_LOOKUP[int(match.group(4))], int(match.group(3), 16)
        case _: raise Exception(part)

part = int(sys.argv[2])
with open(sys.argv[1]) as f:
    instructions = [parse_line(l.rstrip(), part) for l in f]

x = 0
y = 0

vertical_starts = collections.defaultdict(set)
vertical_ends = collections.defaultdict(set)
horizontal_starts = collections.defaultdict(set)
horizontal_ends = collections.defaultdict(set)

for direction, distance in instructions:
    match direction:
        case 'R':
            horizontal_starts[y].add(x)
            x += distance
            horizontal_ends[y].add(x)
        case 'U':
            vertical_ends[y].add(x)
            y -= distance
            vertical_starts[y].add(x)
        case 'L':
            horizontal_ends[y].add(x)
            x -= distance
            horizontal_starts[y].add(x)
        case 'D':
            vertical_starts[y].add(x)
            y += distance
            vertical_ends[y].add(x)
        case _: raise Exception(direction)

vertical_starts = sorted(vertical_starts.items())
vertical_ends = sorted(vertical_ends.items())

def count(active, horizontal_starts, horizontal_ends):
    starts = [x for x in active[::2]]
    ends = [x for x in active[1::2]]

    actions = collections.defaultdict(list)
    for x in starts:
        actions[x].append('RANGE_START')
    for x in ends:
        actions[x+1].append('RANGE_END')
    for x in horizontal_starts:
        actions[x].append('HORIZONTAL_START')
    for x in horizontal_ends:
        actions[x+1].append('HORIZONTAL_END')

    last_x = 0
    active_count = 0
    combined_count = 0
    range_active = False
    horizontal_active = False
    for x, row_actions in sorted(actions.items()):
        if range_active:
            active_count += x - last_x

        if range_active or horizontal_active:
            combined_count += x - last_x

        for action in row_actions:
            match action:
                case 'RANGE_START': range_active = True
                case 'RANGE_END': range_active = False
                case 'HORIZONTAL_START': horizontal_active = True
                case 'HORIZONTAL_END': horizontal_active = False
                case _: raise Exception(y)

        last_x = x

    return active_count, combined_count

active = set()
answer = 0
y = vertical_starts[0][0]
while True:
    if vertical_starts and vertical_starts[0][0] == y:
        active = active.union(vertical_starts.pop(0)[1])

    if vertical_ends[0][0] == y:
        active = active - vertical_ends.pop(0)[1]

    active_count, combined_count = count(sorted(active), horizontal_starts[y], horizontal_ends[y])

    answer += combined_count

    if not vertical_ends:
        break

    if vertical_starts:
        next_y = min(vertical_starts[0][0], vertical_ends[0][0])
    else:
        next_y = vertical_ends[0][0]

    rows_to_skip = next_y - y - 1
    answer += rows_to_skip * active_count

    y = next_y

print(answer)
