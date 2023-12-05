#!/usr/bin/env python3

import sys

def parse_range(l):
    dest, source, length = [int(x) for x in l.split()]
    return (source, source + length, dest - source)

def parse_map(lines):
    source, dest = lines[0].split()[0].split('-to-')
    ranges = [parse_range(l) for l in lines[1:]]

    return source, dest, ranges

def apply(d, active_map):
    for source_start, source_end, diff in active_map:
        if d >= source_start and d < source_end:
            return d + diff

    return d
        
with open(sys.argv[1]) as f:
    data = [int(s) for s in f.readline().split(': ')[1].split()]
    f.readline()

    maps = {source: (dest, ranges) for source, dest, ranges in [parse_map(c.split('\n')) for c in f.read().rstrip().split('\n\n')]}

current_type = 'seed'
while current_type != 'location':
    data = [apply(d, maps[current_type][1]) for d in data]
    current_type = maps[current_type][0]

print(min(data))
