#!/usr/bin/env python3

import functools
import sys

def parse_line(l, repeats):
    springs, target = l.split()
    springs = '?'.join([springs] * repeats)
    target = ','.join([target] * repeats)
    return springs, tuple(int(x) for x in target.split(','))

def recurse_dot(current_run, springs, target):
    if current_run is None:
        return recurse(None, springs[1:], target)
    else:
        if target[0] != current_run:
            return 0
        return recurse(None, springs[1:], target[1:])

def recurse_hash(current_run, springs, target):
    if current_run is None:
        if len(target) == 0:
            return 0
        return recurse(1, springs[1:], target)
    else:
        if current_run == target[0]:
            return 0
        return recurse(current_run + 1, springs[1:], target)

@functools.cache
def recurse(current_run, springs, target):
    if springs:
        match springs[0]:
            case '.': r = recurse_dot(current_run, springs, target)
            case '#': r = recurse_hash(current_run, springs, target)
            case '?': r = recurse_dot(current_run, springs, target) + recurse_hash(current_run, springs, target)
    else:
        if current_run is None:
            r = 1 if not target else 0
        else:
            r = 1 if len(target) == 1 and current_run == target[0] else 0

    return r

def main():
    repeats = int(sys.argv[2])
    with open(sys.argv[1]) as f:
        puzzle = [parse_line(l, repeats) for l in f]

    print(sum(recurse(None, springs, target) for springs, target in puzzle))

if __name__ == '__main__':
    main()
