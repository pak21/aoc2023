#!/usr/bin/env python3

import collections
import graphviz
import sys

def parse_line(l):
    a, bs = l.split(': ')
    return a, set(bs.split(' '))

with open(sys.argv[1]) as f:
    wires = [parse_line(l.rstrip()) for l in f]

links = collections.defaultdict(set)
gv = graphviz.Graph(engine='neato')

for src, dests in wires:
    links[src] |= dests
    for dest in dests:
        links[dest].add(src)
        gv.edge(src, dest)

gv.render(directory='output', format='png', view=True)

match len(links):
    case 15: to_break = [('hfx', 'pzl'), ('bvb', 'cmg'), ('nvd', 'jqt')]
    case 1547: to_break = [('ldk', 'bkm'), ('rsm', 'bvc'), ('zmq', 'pgh')]
    case _: raise Exception(len(links))

for a, b in to_break:
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

print(len(seen) * (len(links) - len(seen)))
