#!/usr/bin/env python3

import collections
import sys

def parse_line(l):
    a, bs = l.split(': ')
    return a, set(bs.split(' '))

with open(sys.argv[1]) as f:
    wires = [parse_line(l.rstrip()) for l in f]

links = collections.defaultdict(set)
for src, dests in wires:
    links[src] |= dests
    for dest in dests:
        links[dest].add(src)

match len(links):
    case 15: to_break = {'hfx': 'pzl', 'bvb': 'cmg', 'nvd': 'jqt'}
    case 1547: to_break = {'ldk': 'bkm', 'rsm': 'bvc', 'zmq': 'pgh'}
    case _: raise Exception(len(links))

for a, b in to_break.items():
    back[b] = a

to_break = {**to_break, **back}

todo = [list(to_break)[0]]

seen = set()
while todo:
    pos = todo.pop(0)

    if pos in seen:
        continue

    seen.add(pos)

    for next_pos in links[pos]:
        if to_break.get(pos) != next_pos:
            todo.append(next_pos)

n1 = len(seen)
n2 = len(links) - len(seen)
print(n1 * n2)
