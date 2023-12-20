#!/usr/bin/env python3

import abc
import dataclasses
import math
import sys

@dataclasses.dataclass
class Pulse:
    src: str
    dest: str
    level: bool

class Module(abc.ABC):
    @abc.abstractmethod
    def accept(self, pulse):
        pass

@dataclasses.dataclass
class BroadcastModule(Module):
    outputs: list[str]

    def accept(self, pulse):
        return [Pulse(pulse.dest, o, pulse.level) for o in self.outputs]

@dataclasses.dataclass
class FlipFlopModule(Module):
    module_state: bool
    outputs: list[str]

    def accept(self, pulse):
        if pulse.level: return []

        self.module_state = not self.module_state
        return [Pulse(pulse.dest, o, self.module_state) for o in self.outputs]

@dataclasses.dataclass
class ConjunctionModule(Module):
    module_state: dict[str, bool]
    outputs: list[str]

    def accept(self, pulse):
        self.module_state[pulse.src] = pulse.level
        output = not all(self.module_state.values())
        return [Pulse(pulse.dest, o, output) for o in self.outputs]

def parse_module(l):
    prefix, suffix = l.split(' -> ')
    outputs = suffix.split(', ')

    match prefix[0]:
        case '%':
            mn = prefix[1:]
            module = FlipFlopModule(False, outputs)
        case '&':
            mn = prefix[1:]
            module = ConjunctionModule({}, outputs)
        case _ if prefix == 'broadcaster':
            mn = prefix
            module = BroadcastModule(outputs)
        case _: raise Exception(prefix)

    return mn, module

def parse(fn):
    with open(fn) as f:
        modules = dict([parse_module(l.rstrip()) for l in f])

    for name, module in modules.items():
        for output in module.outputs:
            if output in modules and isinstance(modules[output], ConjunctionModule):
                modules[output].module_state[name] = False

    return modules

def main():
    modules = parse(sys.argv[1])

    output_inverter = [m for m in modules.items() if 'rx' in m[1].outputs]
    if len(output_inverter) != 1 :
        raise Exception(f'More than one module connected to rx: {output_inverter}')
    output_inverter = output_inverter[0]
    if not isinstance(output_inverter[1], ConjunctionModule):
        raise Exception(f'Expected output inverter is not an inverter: {output_inverter}')

    watches = output_inverter[1].module_state.keys()
    print(f'Watching {watches} for Part 2')

    periods = {}

    n = 0
    counts = {False: 0, True: 0}
    while len(periods) != len(watches):
        n += 1
        todo = [Pulse('button', 'broadcaster', False)]
        while todo:
            pulse = todo.pop(0)

            counts[pulse.level] += 1

            if pulse.src in watches and pulse.level:
                print(f'{pulse.src} went high after {n} presses')
                periods[pulse.src] = n

            if pulse.dest in modules:
                todo += modules[pulse.dest].accept(pulse)

        if n == 1000:
            print('Part 1:', counts[False] * counts[True])

    print(f'Output will go low after {math.lcm(*periods.values())} presses')

if __name__ == '__main__':
    main()
