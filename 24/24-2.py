#!/usr/bin/env python3

import dataclasses
import sys

import sympy

@dataclasses.dataclass
class Hailstone:
    pos: list[int]
    vel: list[int]

def parse_line(l):
    prefix, suffix = l.split(' @ ')
    pos = [int(a) for a in prefix.split(', ')]
    vel = [int(a) for a in suffix.split(', ')]
    return Hailstone(pos, vel)

def parse(fn):
    with open(fn) as f:
        return [parse_line(l.rstrip()) for l in f]

def make_equation(h, n, i, r, v, t):
    print(f'Adding (r{i} + v{i} * t{n}) - ({h.pos[i]} + {h.vel[i]} * t{n}) = 0')
    return (r[i] + v[i] * t[n]) - (h.pos[i] + h.vel[i] * t[n])

def main():
    hailstones = parse(sys.argv[1])

    r = sympy.symbols('r0 r1 r2')
    v = sympy.symbols('v0 v1 v2')
    t = sympy.symbols('t0 t1 t2')
    equations = [make_equation(h, n, i, r, v, t) for n, h in enumerate(hailstones[:3]) for i in range(3)]
    print()

    solution = sympy.solve(equations, dict=True)
    if len(solution) != 1:
        raise Exception(f'Multiple solutions found: {solution}')
    solution = solution[0]

    for variable, value in solution.items():
        print(f'{variable} = {value}')
    print()

    print(sum(solution[a] for a in r))

if __name__ == '__main__':
    main()
