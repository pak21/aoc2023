#!/usr/bin/env python3

import functools
import math
import operator
import sys

def do_race(time, distance):
    # Distance travelled s = b * (T - b) = -b^2 + Tb where b = time button held down, T = total race time
    # We want to solve s = D where D = race record, so therefore -b^2 + Tb - D = 0 or b^2 - Tb + D = 0
    #
    # Or expressing in terms of the standard quadratic formula a = 1, b = -T, c = D
    discriminant = math.sqrt(time * time - 4 * distance)
    lower_root = (time - discriminant) / 2
    upper_root = (time + discriminant) / 2

    # Hacky shenanigans to deal with the test case of (30, 200) which has integer roots
    lower_answer = lower_root + 1 if lower_root == int(lower_root) else math.ceil(lower_root)
    upper_answer = upper_root - 1 if upper_root == int(upper_root) else math.floor(upper_root)

    return upper_answer - lower_answer + 1

with open(sys.argv[1]) as f:
    times = [int(x) for x in f.readline().split()[1:]]
    distances = [int(x) for x in f.readline().split()[1:]]

print(functools.reduce(operator.mul, (do_race(time, distance) for time, distance in zip(times, distances))))

part2_time = int(functools.reduce(operator.add, (str(x) for x in times)))
part2_distance = int(functools.reduce(operator.add, (str(x) for x in distances)))

print(do_race(part2_time, part2_distance))
