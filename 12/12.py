#!/usr/bin/env python3

import sys

def parse_line(l):
    springs, result = l.split()
    return [' ' if c == '.' else c for c in springs], [int(x) for x in result.split(',')]

def score_line(springs):
    return [len(s) for s in ''.join(springs).split()]

def eval_line(springs, result):
    unknowns = [i for i, c in enumerate(springs) if c == '?']

    good = 0
    for i in range(2**len(unknowns)):
        for j, n in enumerate(unknowns):
            springs[n] = '#' if i & (2**j) else ' '
        if score_line(springs) == result:
            good += 1

    return good

with open(sys.argv[1]) as f:
    puzzle = [parse_line(l) for l in f]

part1 = 0
for springs, result in puzzle:
    foo = ''.join(springs).replace(' ', '.')
    r = eval_line(springs, result)
    print(foo, r)
    part1 += r

print(part1)
