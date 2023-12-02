#!/usr/bin/env python3

import collections
import functools
import sys

def parse_show(s):
    return collections.defaultdict(int, {b: int(a) for a, b in [p.split(' ') for p in s.split(', ')]})

def parse_game(l):
    foo, bar = l.split(': ')
    game_id = int(foo[4:])
    return (game_id, [parse_show(s) for s in bar.split('; ')])

LIMITS = {'red': 12, 'green': 13, 'blue': 14}
def check_part1(shows):
    for show in shows:
        for c, l in LIMITS.items():
            if show[c] > l:
                return False
    
    return True

def power(shows):
    mins = collections.defaultdict(int)
    for show in shows:
        for c in LIMITS:
            if mins[c] < show[c]:
                mins[c] = show[c]
    return functools.reduce(lambda a, b: a * b, mins.values())

with open(sys.argv[1]) as f:
    games = [parse_game(l.rstrip()) for l in f.readlines()]

print(sum([game_id for game_id, shows in games if check_part1(shows)]))
print(sum([power(shows) for _, shows in games]))
