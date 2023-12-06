#!/usr/bin/env python3

import sys

def do_race(time, distance):
    good = 0
    for speed in range(0, time+1):
        time_left = time - speed
        travelled = speed * time_left
        if travelled > distance:
            good += 1

    return good

with open(sys.argv[1]) as f:
    times_l = f.readline()
    distances_l = f.readline()

times = [int(x) for x in times_l.split()[1:]]
distances = [int(x) for x in distances_l.split()[1:]]

races = list(zip(times, distances))

part1 = 1
for time, distance in races:
    ways = do_race(time, distance)
    part1 *= ways

print(part1)
