#!/usr/bin/env python3

import sys

rounded = set()
cubes = set()

with open(sys.argv[1]) as f:
    for y, row in enumerate(f):
        for x, c in enumerate(row):
            match c:
                case '.': pass
                case 'O': rounded.add((x, y))
                case '#': cubes.add((x,y))

max_x = x
max_y = y + 1

def tilt(before, step, select_fn, build_fn, max_value):
    after = before.copy()
    for rock in after.copy():
        i = select_fn(rock)
        last_empty = i
        while i >= 0 and i < max_value:
            new_pos = build_fn(rock, i)
            if new_pos in cubes:
                break

            if new_pos not in after:
                last_empty = i

            i += step

        after.remove(rock)
        after.add(build_fn(rock, last_empty))

    return after

def tilt_x(before, step):
    return tilt(before, step, lambda r: r[0], lambda r, i: (i, r[1]), max_x)

def tilt_y(before, step):
    return tilt(before, step, lambda r: r[1], lambda r, i: (r[0], i), max_y)

def east(before):
    return tilt_x(before, 1)

def north(before):
    return tilt_y(before, -1)

def west(before):
    return tilt_x(before, -1)

def south(before):
    return tilt_y(before, 1)

def spin(before):
    return east(south(west(north(before))))

def score(rounded):
    return max_y * len(rounded) - sum(r[1] for r in rounded)

print(score(north(rounded)))

seen = {tuple(rounded): 0}
answers = [score(rounded)]

spins = 0
while True:
    rounded = spin(rounded)
    spins += 1
    t = tuple(rounded)
    if t in seen:
        period = spins - seen[t]
        key = seen[t] + ((1000000000 - seen[t]) % period)
        print(answers[key])
        break

    seen[t] = spins
    answers.append(score(rounded))
