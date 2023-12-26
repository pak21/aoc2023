#!/usr/bin/env python3

import collections
import operator
import random
import sys

def parse_line(l):
    a, bs = l.split(': ')
    return a, set(bs.split(' '))

def find_shortest_path(links, start, end):
    todo = [(start, [])]
    seen = set()

    shortest = None
    while todo:
        pos, path = todo.pop(0)

        if pos in seen:
            continue

        seen.add(pos)
        next_path = path + [pos]

        if pos == end:
            return zip(next_path, next_path[1:])

        for next_pos in links[pos]:
            todo.append((next_pos, next_path))

    raise Exception(f'No path found from {start} to {end}?')

def find_connected_set(links, to_break):
    todo = [list(links)[0]]

    seen = set()
    while todo:
        pos = todo.pop(0)

        if pos in seen:
            continue

        seen.add(pos)

        for next_pos in links[pos]:
            if (pos, next_pos) not in to_break and (next_pos, pos) not in to_break:
                todo.append(next_pos)

    return len(seen)

with open(sys.argv[1]) as f:
    wires = [parse_line(l.rstrip()) for l in f]

links = collections.defaultdict(set)
for src, dests in wires:
    links[src] |= dests
    for dest in dests:
        links[dest].add(src)

nodes = list(links.keys())

traversed = collections.defaultdict(int)
i = 0
while True:
    i += 1
    start = nodes[random.randrange(len(nodes))]
    end = nodes[random.randrange(len(nodes))]

    for a, b in find_shortest_path(links, start, end):
        key = (a, b) if a < b else (b, a)
        traversed[key] += 1

    to_break = set([pair for pair, _ in sorted(traversed.items(), key=operator.itemgetter(1))[-3:]])

    connected_count = find_connected_set(links, to_break)

    if connected_count != len(links):
        print(f'Found a partition after {i} iterations: {to_break}')
        print(connected_count * (len(links) - connected_count))
        break
