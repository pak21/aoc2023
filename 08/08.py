#!/usr/bin/env python3

import math
import re
import sys

def parse_node(l):
    m = re.match('(...) = \((...), (...)\)', l)
    return m.groups()

def run_camel(camel):
    moves = 0
    while camel[-1] != 'Z':
        move = 0 if instructions[moves % len(instructions)] == 'L' else 1
        camel = nodes[camel][move]
        moves += 1

    return moves

with open(sys.argv[1]) as f:
    instructions = list(f.readline().rstrip())
    f.readline()
    nodes = {loc: (l, r) for loc, l, r, in (parse_node(l) for l in f.readlines())}

# This happens to work, this camel never reaches a node which matches '..Z' but isn't 'ZZZ'
print(run_camel('AAA'))
print(math.lcm(*[run_camel(n) for n in nodes if n[-1] == 'A']))
