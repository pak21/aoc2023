#!/usr/bin/env python3

import sys

def make_rows(values):
    rows = [values]
    while not all((x == 0 for x in rows[-1])):
        new_row = [b - a for a, b in zip(rows[-1][:-1], rows[-1][1:])]
        rows.append(new_row)

    return rows

def part2(rows):
    prev = 0
    for a in reversed([r[0] for r in rows]):
        prev = a - prev

    return prev

with open(sys.argv[1]) as f:
    lines = [[int(x) for x in l.split()] for l in f.readlines()]

row_sets = [make_rows(l) for l in lines]

print(sum(r[-1] for rows in row_sets for r in rows))
print(sum(part2(rows) for rows in row_sets))
