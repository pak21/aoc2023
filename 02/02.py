#!/usr/bin/env python3

import collections
import functools
import operator
import sys

def parse_show(s):
    return collections.defaultdict(int, {b: int(a) for a, b in [p.split() for p in s.split(', ')]})

def parse_game(l):
    foo, bar = l.split(': ')
    return (int(foo[4:]), [parse_show(s) for s in bar.split('; ')])

LIMITS = {'red': 12, 'green': 13, 'blue': 14}
def check_part1(shows):
    return all(
        not any(
            show[c] > l
            for c, l
            in LIMITS.items()
        )
        for show
        in shows
    )

def power(shows):
    return functools.reduce(
        operator.mul, 
        (
            max(shows, key=operator.itemgetter(c))[c]
            for c
            in LIMITS
        )
    )

with open(sys.argv[1]) as f:
    games = [parse_game(l.rstrip()) for l in f.readlines()]

print(sum([game_id for game_id, shows in games if check_part1(shows)]))
print(sum([power(shows) for _, shows in games]))
