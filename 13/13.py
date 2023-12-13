#!/usr/bin/env python3

import sys

def parse_pattern(lines):
    return [[c == '#' for c in row] for row in lines.split('\n')]

def rotate(pattern):
    return [[pattern[y][x] for y in range(len(pattern))] for x in range(len(pattern[0]))]

def find_mirror(pattern, old):
    for y in range(1, len(pattern)):
        if y == old:
            continue
        above=pattern[y-1::-1]
        below=pattern[y:]

        if all(a == b for a, b in zip(pattern[y-1::-1], pattern[y:])):
            return y

    return None

def find_reflection(pattern, old_line=None):
    old_horizontal = old_line[1] if old_line and old_line[0] else None
    horizontal = find_mirror(pattern, old_horizontal)
    if horizontal is not None:
        return (True, horizontal)

    old_vertical = old_line[1] if old_line and not old_line[0] else None
    vertical = find_mirror(rotate(pattern), old_vertical)
    if vertical is not None:
        return (False, vertical)

    return None

def score(lines):
    return sum((100 if h else 1) * l for h, l in lines)

def try_smudge(pattern, x, y, old_line):
    pattern[y][x] = not pattern[y][x]
    new_line = find_reflection(pattern, old_line)
    pattern[y][x] = not pattern[y][x]

    return new_line

def try_smudges(pattern, old_line):
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            new_line = try_smudge(pattern, x, y, old_line)
            if new_line is not None:
                return new_line

with open(sys.argv[1]) as f:
    patterns = [parse_pattern(lines.rstrip()) for lines in f.read().split('\n\n')]

# TODO: cache the rotated pattern

lines = [find_reflection(p) for p in patterns]
print(score(lines))

new_lines = [try_smudges(p, l) for p, l in zip(patterns, lines)]
print(score(new_lines))
