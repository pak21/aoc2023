#!/usr/bin/env python3

import collections
import operator
import random
import sys

def parse_line(l):
    a, bs = l.split(': ')
    return a, set(bs.split(' '))

random.seed(42)

with open(sys.argv[1]) as f:
    wires = [parse_line(l.rstrip()) for l in f]

links = collections.defaultdict(set)
for src, dests in wires:
    links[src] |= dests
    for dest in dests:
        links[dest].add(src)

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

    to_break = sorted(traversed.items(), key=operator.itemgetter(1))[-3:]

    for (a, b), _ in to_break:
        links[a].remove(b)
        links[b].remove(a)

    todo = [list(links)[0]]

    seen = set()
    while todo:
        pos = todo.pop(0)

        if pos in seen:
            continue

        seen.add(pos)

        for next_pos in links[pos]:
            todo.append(next_pos)

    if len(seen) != len(links):
        print(f'Found a partition after {i} iterations: {to_break}')
        print(len(seen) * (len(links) - len(seen)))
        break

    for (a, b), _ in to_break:
        links[a].add(b)
        links[b].add(a)
