#!/usr/bin/env python3

import dataclasses
import sys

@dataclasses.dataclass
class Brick:
    start: list[int, int, int]
    end: list[int, int, int]

def parse_coords(s):
    return [int(i) for i in s.split(',')]

def parse_brick(l):
    start_s, end_s = l.split('~')
    start = parse_coords(start_s)
    end = parse_coords(end_s)

    return Brick(start, end)

def do_overlap(b1, b2):
    if b1.start[0] > b2.end[0] or b2.start[0] > b1.end[0]:
        return False

    if b1.start[1] > b2.end[1] or b2.start[1] > b1.end[1]:
        return False

    return True

def make_overlaps(bricks):
    return {(i, j): do_overlap(b1, b2) for i, b1 in enumerate(bricks) for j, b2 in enumerate(bricks)}

def parse(fn):
    with open(fn) as f:
        return [parse_brick(l.rstrip()) for l in f]

def does_block(i, j, b1, b2, overlaps):
    return b2.end[2] == b1.start[2] - 1 and overlaps[i, j]

def fall(bricks, overlaps):
    has_moved = True
    while has_moved:
        has_moved = False

        for i, brick in enumerate(bricks):
            start_z = brick.start[2]
            if start_z == 1:
                continue

            if not any(does_block(i, j, brick, b2, overlaps) for j, b2 in enumerate(bricks))
                brick.start[2] -= 1
                brick.end[2] -= 1
                has_moved = True

def disintegrate(supporter_count_orig, does_support, to_disintegrate):
    supporter_count = supporter_count_orig.copy()

    todo = [to_disintegrate]

    n = 0
    while todo:
        i = todo.pop(0)
        n += 1
        for j in does_support[i]:
            supporter_count[j] -= 1
            if supporter_count[j] == 0:
                todo.append(j)

    return n - 1

def main():
    bricks = parse(sys.argv[1])
    overlaps = make_overlaps(bricks)

    fall(bricks, overlaps)

    can_disintegrate = [True] * len(bricks)
    supporter_count = [None] * len(bricks)
    does_support = [set() for _ in range(len(bricks))]
    for i, b in enumerate(bricks):
        brick_supports = [j for j, b2 in enumerate(bricks) if does_block(i, j, b, b2, overlaps)]
        supporter_count[i] = len(brick_supports)
        if len(brick_supports) == 1:
            can_disintegrate[brick_supports[0]] = False
        for s in brick_supports:
            does_support[s].add(i)

    print(sum(can_disintegrate))
    print(sum(disintegrate(supporter_count, does_support, i) for i in range(len(bricks))))

if __name__ == '__main__':
    main()
