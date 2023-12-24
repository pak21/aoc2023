#!/usr/bin/env python3

import dataclasses
import itertools
import sys

@dataclasses.dataclass
class Line:
    # y = mx + c
    m: float
    c: float

    def calc(self, x):
        return self.m * x + self.c

@dataclasses.dataclass
class Hailstone:
    pos: list[int]
    vel: list[int]

    equation: Line

def parse_line(l):
    prefix, suffix = l.split(' @ ')
    pos = [int(a) for a in prefix.split(', ')]
    vel = [int(a) for a in suffix.split(', ')]
    return Hailstone(pos, vel, None)

def parse(fn):
    with open(fn) as f:
        return [parse_line(l.rstrip()) for l in f]

def make_line(h):
    t_x_0 = -h.pos[0] / h.vel[0]
    c = h.pos[1] + (h.vel[1] * t_x_0)
    m = h.vel[1] / h.vel[0]

    return Line(m, c)

def intercept(a, b):
    if a.equation.m == b.equation.m:
        if a.equation.c == b.equation.c:
            raise Exception(a, b)

        return None

    x = (b.equation.c - a.equation.c) / (a.equation.m - b.equation.m)
    y1 = a.equation.calc(x)

    return x, a.equation.calc(x)

def time_for_x(h, x):
    # x = x0 + v_x * t
    # => t = (x - x0) / v_x

    return (x - h.pos[0]) / h.vel[0]

def main():
    hailstones = parse(sys.argv[1])

    match len(hailstones):
        case 5:
            range_start = 7
            range_end = 27
        case 300:
            range_start = 200000000000000
            range_end = 400000000000000
        case _: raise Exception(len(hailstones))

    for h in hailstones:
        h.equation = make_line(h)

    count = 0
    for a, b in itertools.combinations(hailstones, 2):
        ip = intercept(a, b)

        if ip:
            if ip[0] >= range_start and ip[0] <= range_end and ip[1] >= range_start and ip[1] <= range_end:
                a_time = time_for_x(a, ip[0])
                b_time = time_for_x(b, ip[0])
                if a_time >= 0 and b_time >= 0:
                    count += 1

    print(count)

if __name__ == '__main__':
    main()
