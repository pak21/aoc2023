#!/usr/bin/env python3

import bisect
import itertools
import sys

def calc_dists(v1, v2, expands):
    v_min, v_max = (v1, v2) if v1 < v2 else (v2, v1)

    start_idx = bisect.bisect_left(expands, v_min)
    end_idx = bisect.bisect_left(expands, v_max, lo=start_idx)

    return v_max - v_min, end_idx - start_idx

def calc(vs):
    expands = sorted(set(range(max(vs))) - set(vs))

    return list(
        map(
            sum, 
            zip(*(
                calc_dists(v1, v2, expands)
                for v1, v2 in itertools.combinations(vs, 2)
            ))
        )
    )

xs = []
ys = []

with open(sys.argv[1]) as f:
    for y, l in enumerate(f):
        for x, c in enumerate(l):
            if c == '#':
                xs.append(x)
                ys.append(y)

x_dists = calc(xs)
y_dists = calc(ys)

print(x_dists[0] + x_dists[1] + y_dists[0] + y_dists[1])
print(x_dists[0] + 999999 * x_dists[1] + y_dists[0] + 999999 * y_dists[1])
