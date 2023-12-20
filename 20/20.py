#!/usr/bin/env python3

import enum
import math
import sys

class ModuleType(enum.Enum):
    BROADCASTER = enum.auto(),
    FLIPFLOP = enum.auto(),
    CONJUNCTION = enum.auto(),

def parse_module(l):
    prefix, suffix = l.split(' -> ')
    match prefix[0]:
        case '%':
            mn = prefix[1:]
            mt = ModuleType.FLIPFLOP
            ms = False
        case '&':
            mn = prefix[1:]
            mt = ModuleType.CONJUNCTION
            ms = {}
        case _ if prefix == 'broadcaster':
            mn = prefix
            mt = ModuleType.BROADCASTER
            ms = None
        case _: raise Exception(prefix)

    outputs = suffix.split(', ')

    return mn, (mt, ms, outputs)

def parse(fn):
    with open(fn) as f:
        modules = dict([parse_module(l.rstrip()) for l in f])

    for mn, (mt, ms, outputs) in modules.items():
        for output in outputs:
            if output in modules and modules[output][0] == ModuleType.CONJUNCTION:
                modules[output][1][mn] = False

    return modules

def send_pulse(modules, src, dest, high):
#    print(f'{src} -{"high" if high else "low"}-> {dest}')
    if dest not in modules:
        return []

    mt, ms, outputs = modules[dest]
    match mt:
        case ModuleType.FLIPFLOP:
            if high:
                pulses = []
            else:
                ms = not ms
                modules[dest] = (mt, ms, outputs)
                pulses = [(dest, o, ms) for o in outputs]

        case ModuleType.CONJUNCTION:
            ms[src] = high
            modules[dest] = (mt, ms, outputs)
            output = not all(ms.values())
            pulses = [(dest, o, output) for o in outputs]

        case _: raise Exception(mt)

    return pulses

def main():
    modules = parse(sys.argv[1])

    output_inverter = [m for m in modules.items() if 'rx' in m[1][2]]
    if len(output_inverter) != 1 :
        raise Exception(f'More than one module connected to rx: {output_inverter}')
    output_inverter = output_inverter[0]
    if output_inverter[1][0] != ModuleType.CONJUNCTION:
        raise Exception(f'Expected output inverter is not an inverter: {output_inverter}')

    watches = output_inverter[1][1].keys()
    print(f'Watching {watches} for Part 2')

    periods = {}

    n = 0
    counts = {False: 0, True: 0}
    while len(periods) != len(watches):
        n += 1
        counts[False] += 1 # button to broadcaster
        todo = [('broadcaster', o, False) for o in modules['broadcaster'][2]]
        while todo:
            src, dest, high = todo.pop(0)

            counts[high] += 1

            if src in watches and high:
                print(f'{src} went high after {n} presses')
                periods[src] = n

            pulses = send_pulse(modules, src, dest, high)
            todo += pulses

        if n == 1000:
            print('Part 1:', counts[False] * counts[True])

    print(f'Output will go low after {math.lcm(*periods.values())} presses')

if __name__ == '__main__':
    main()
