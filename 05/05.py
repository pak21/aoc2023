#!/usr/bin/env python3

import sys

def parse_seeds(l):
    _, seeds = l.split(': ')
    return [int(s) for s in seeds.split()]

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
        ranges = [parse_range(l) for l in lines[1:] if l]

        maps[source] = (dest, ranges)

    return maps

def apply_one(d, active_map):
    for dest_start, source_start, length in active_map:
        if d >= source_start and d < source_start + length:
            return dest_start + (d - source_start)

    return d
        
def apply(data, active_map):
    return [apply_one(d, active_map) for d in data]

with open(sys.argv[1]) as f:
    data = parse_seeds(f.readline().rstrip())
    f.readline()

    maps = parse_maps(f.read().split('\n\n'))

current_type = 'seed'
while current_type != 'location':
    data = apply(data, maps[current_type][1])
    current_type = maps[current_type][0]

print(min(data))
