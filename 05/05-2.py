#!/usr/bin/env python3

import functools
import operator
import sys

def parse_seed_ranges(l):
    _, data = l.split(': ')
    numbers = [int(x) for x in data.split()]
    starts = numbers[::2]
    lengths = numbers[1::2]
    return [(s, s+l) for s, l in zip(starts, lengths)]

def parse_header(l):
    data, _ = l.split()
    return data.split('-to-')

def parse_range(l):
    return [int(x) for x in l.split()]

def parse_maps(chunks):
    maps = {}
    for chunk in chunks:
        lines = chunk.split('\n')
        source, dest = parse_header(lines[0])
        ranges = sorted([parse_range(l) for l in lines[1:] if l], key=operator.itemgetter(1))

        maps[source] = (dest, ranges)

    return maps

def apply_one(data_start, data_end, active_map):
    new_data = []
    current_pos = data_start
    for dest_start, source_start, mapping_length in active_map:
        if source_start >= data_end:
            break

        source_end = source_start + mapping_length
        if source_end < data_start:
            continue

        new_data.append((current_pos, source_start))

        start_point = max(current_pos, source_start)
        end_point = min(source_end, data_end)

        diff = dest_start - source_start

        new_data.append((start_point + diff, end_point + diff))

        current_pos = end_point

    new_data.append((current_pos, data_end))

    return [x for x in new_data if x[0] < x[1]]

def apply(data, active_map):
    xs = [apply_one(ds, de, active_map) for ds, de in data]
    y = functools.reduce(operator.add, xs)
    return y

with open(sys.argv[1]) as f:
    data = parse_seed_ranges(f.readline().rstrip())
    f.readline()

    maps = parse_maps(f.read().split('\n\n'))

current_type = 'seed'
while current_type != 'location':
    data = apply(data, maps[current_type][1])
    current_type = maps[current_type][0]

print(min(data, key=operator.itemgetter(0))[0])
