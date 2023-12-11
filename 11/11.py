#!/usr/bin/env python3

import bisect
import itertools
import sys

def calc_dists(v1, v2, expands):
    v_min, v_max = (v1, v2) if v1 < v2 else (v2, v1)

    start_idx = bisect.bisect_left(expands, v_min)
    end_idx = bisect.bisect_left(expands, v_max, lo=start_idx)

    return v_max - v_min, end_idx - start_idx

def calc(vs, v_set):
    expands = sorted(set(range(max(v_set))) - v_set)

    dists = [
        calc_dists(v1, v2, expands)
        for v1, v2 in itertools.combinations(vs, 2)
    ]

    return sum(d[0] for d in dists), sum(d[1] for d in dists)

xs = []
x_values = set()

ys = []
y_values = set()

with open(sys.argv[1]) as f:
    for y, l in enumerate(f):
        for x, c in enumerate(l):
            if c == '#':
                xs.append(x)
                x_values.add(x)

                ys.append(y)
                y_values.add(y)

x_dists = calc(xs, x_values)
y_dists = calc(ys, y_values)

print(x_dists[0] + x_dists[1] + y_dists[0] + y_dists[1])
print(x_dists[0] + 999999 * x_dists[1] + y_dists[0] + 999999 * y_dists[1])
