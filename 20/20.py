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
    state: bool
    outputs: list[str]

    def accept(self, pulse):
        if pulse.level: return []

        self.state = not self.state
        return [Pulse(pulse.dest, o, self.state) for o in self.outputs]

@dataclasses.dataclass
class ConjunctionModule(Module):
    inputs: dict[str, bool]
    outputs: list[str]

    def accept(self, pulse):
        self.inputs[pulse.src] = pulse.level
        output = not all(self.inputs.values())
        return [Pulse(pulse.dest, o, output) for o in self.outputs]

def parse_module(l):
    prefix, suffix = l.split(' -> ')
    outputs = suffix.split(', ')

    match prefix[0]:
        case '%':
            name = prefix[1:]
            module = FlipFlopModule(False, outputs)
        case '&':
            name = prefix[1:]
            module = ConjunctionModule({}, outputs)
        case _ if prefix == 'broadcaster':
            name = prefix
            module = BroadcastModule(outputs)
        case _: raise Exception(prefix)

    return name, module

def parse(fn):
    with open(fn) as f:
        modules = dict(parse_module(l.rstrip()) for l in f)

    for name, module in modules.items():
        for output in module.outputs:
            if output in modules and isinstance(modules[output], ConjunctionModule):
                modules[output].inputs[name] = False

    return modules

def main():
    modules = parse(sys.argv[1])

    print('digraph{')
    for name, module in modules.items():
        if isinstance(module, FlipFlopModule):
            print(f'{name} -> {{{",".join(module.outputs)}}}')
        elif isinstance(module, ConjunctionModule):
            print(f'{name} -> {{{",".join(module.outputs)}}}')
        elif isinstance(module, BroadcastModule):
            print(f'{name} -> {{{",".join(module.outputs)}}}')
        else:
            raise Exception(name, module)
    print('}')

#    return

    part1_only = False
    watches = {}
    output_inverter = [m for m in modules.items() if 'rx' in m[1].outputs]
    match len(output_inverter):
        case 0:
            print(f"No rx output found, assuming we're using test data")
            part1_only = True

        case 1:
            output_inverter = output_inverter[0]
            if not isinstance(output_inverter[1], ConjunctionModule):
                raise Exception(f'Expected output inverter is not an inverter: {output_inverter}')
            watches = output_inverter[1].inputs.keys()
            periods = {}
            print(f'Watching {watches} for Part 2')

        case _:
            raise Exception(f'More than one module connected to rx: {output_inverter}')

    n = 0
    counts = {False: 0, True: 0}
    done = False
    while not done:
        n += 1
        todo = [Pulse('button', 'broadcaster', False)]
        while todo:
            pulse = todo.pop(0)

            counts[pulse.level] += 1

            if pulse.src in watches and pulse.level:
                print(f'{pulse.src} went high after {n} presses')
                periods[pulse.src] = n
                if len(periods) == len(watches):
                    print(f'Output will go low after {math.lcm(*periods.values())} presses')
                    done = True

            if pulse.dest in modules:
                todo += modules[pulse.dest].accept(pulse)

        if n == 1000:
            print('Part 1:', counts[False] * counts[True])
            if part1_only:
                done = True

if __name__ == '__main__':
    main()
