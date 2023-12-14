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

def north(before):
    after = before.copy()
    for rock in after.copy():
        x = rock[0]
        y = rock[1]
        last_empty = y
        while y >= 0:
            if (x, y) in cubes:
                break

            if (x, y) not in after:
                last_empty = y

            y -= 1

        after.remove(rock)
        after.add((x, last_empty))

    return after

def south(before):
    after = before.copy()
    for rock in after.copy():
        x = rock[0]
        y = rock[1]
        last_empty = y
        while y < max_y:
            if (x, y) in cubes:
                break

            if (x, y) not in after:
                last_empty = y

            y += 1

        after.remove(rock)
        after.add((x, last_empty))

    return after

def east(before):
    after = before.copy()
    for rock in after.copy():
        x = rock[0]
        y = rock[1]
        last_empty = x
        while x < max_x:
            if (x, y) in cubes:
                break

            if (x, y) not in after:
                last_empty = x

            x += 1

        after.remove(rock)
        after.add((last_empty, y))

    return after

def west(before):
    after = before.copy()
    for rock in after.copy():
        x = rock[0]
        y = rock[1]
        last_empty = x
        while x >= 0:
            if (x, y) in cubes:
                break

            if (x, y) not in after:
                last_empty = x

            x -= 1

        after.remove(rock)
        after.add((last_empty, y))

    return after

def spin(before):
    return east(south(west(north(before))))

def score(rounded):
    return sum(max_y - r[1] for r in rounded)

part1 = north(rounded)
print(score(part1))

seen = {tuple(rounded): 0}
answers = {}

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
    answers[spins] = score(rounded)
