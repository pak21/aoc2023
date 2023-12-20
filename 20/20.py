#!/usr/bin/env python3

import dataclasses
import enum
import math
import sys

@dataclasses.dataclass
class Pulse:
    src: str
    dest: str
    level: bool

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

def send_pulse(modules, pulse):
#    print(f'{src} -{"high" if high else "low"}-> {dest}')
    if pulse.dest not in modules:
        return []

    mt, ms, outputs = modules[pulse.dest]
    match mt:
        case ModuleType.FLIPFLOP:
            if pulse.level:
                pulses = []
            else:
                ms = not ms
                modules[pulse.dest] = (mt, ms, outputs)
                pulses = [Pulse(pulse.dest, o, ms) for o in outputs]

        case ModuleType.CONJUNCTION:
            ms[pulse.src] = pulse.level
            modules[pulse.dest] = (mt, ms, outputs)
            output = not all(ms.values())
            pulses = [Pulse(pulse.dest, o, output) for o in outputs]

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
        todo = [Pulse('broadcaster', o, False) for o in modules['broadcaster'][2]]
        while todo:
            pulse = todo.pop(0)

            counts[pulse.level] += 1

            if pulse.src in watches and pulse.level:
                print(f'{pulse.src} went high after {n} presses')
                periods[pulse.src] = n

            pulses = send_pulse(modules, pulse)
            todo += pulses

        if n == 1000:
            print('Part 1:', counts[False] * counts[True])

    print(f'Output will go low after {math.lcm(*periods.values())} presses')

if __name__ == '__main__':
    main()
