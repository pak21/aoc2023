#!/usr/bin/env python3

import functools
import operator
import sys

def parse_seed_ranges(l):
    numbers = [int(x) for x in l.split(': ')[1].split()]
    return [(s, s+l) for s, l in zip(numbers[::2], numbers[1::2])]

def parse_range(l):
    dest, source, length = [int(x) for x in l.split()]
    return (source, source + length, dest - source)

def parse_map(lines):
    source, dest = lines[0].split()[0].split('-to-')
    ranges = sorted([parse_range(l) for l in lines[1:]], key=operator.itemgetter(1))

    return source, dest, ranges

def apply(data_start, data_end, active_map):
    new_data = []
    current_pos = data_start
    for source_start, source_end, diff in active_map:
        if source_start >= data_end:
            # This mapping (and hence all future ones as they are stored) is entirely after our data so we can end our work here
            break

        if source_end < data_start:
            # This mapping is entirely before our data so we can skip this and move to the next one
            continue

        # Add any part of our current range which is before the mapping
        if current_pos < source_start:
            new_data.append((current_pos, source_start))

        # The mapped range starts at whichever is later of our current position and the start of the mapping
        start_point = max(current_pos, source_start)
        # The mapped range ends at which is earlier of the end of the mapping and the end of the data
        end_point = min(source_end, data_end)

        # Add the actual mapped range (if any)
        if start_point < end_point:
            new_data.append((start_point + diff, end_point + diff))

        current_pos = end_point

    # Add any part of our current range which is after all mappings
    if current_pos < data_end:
        new_data.append((current_pos, data_end))

    return new_data

with open(sys.argv[1]) as f:
    data = parse_seed_ranges(f.readline())
    f.readline()

    maps = {source: (dest, ranges) for source, dest, ranges in [parse_map(c.split('\n')) for c in f.read().rstrip().split('\n\n')]}

current_type = 'seed'
while current_type != 'location':
    data = functools.reduce(operator.add, [apply(ds, de, maps[current_type][1]) for ds, de in data])
    current_type = maps[current_type][0]

print(min(data, key=operator.itemgetter(0))[0])
