#!/usr/bin/env python3

import dataclasses
import functools
import operator
import sys

@dataclasses.dataclass
class Conditional:
    rating: str
    operator: str
    value: int
    target: str

@dataclasses.dataclass
class Constraint:
    min_value: int
    max_value: int

    def range(self):
        return max(self.max_value - self.min_value + 1, 0)

def parse_conditional(s):
    condition, target = s.split(':')
    return Conditional(condition[0], condition[1], int(condition[2:]), target)

def parse_rules(s):
    strings = s[:-1].split(',')
    conditionals = [parse_conditional(s2) for s2 in strings[:-1]]
    return conditionals, strings[-1]

def parse_workflow(l):
    name, rules_s = l.split('{')
    rules = parse_rules(rules_s)
    return name, rules

def parse_rating(l):
    return dict([(s[0], int(s[2:])) for s in l[1:-1].split(',')])

def parse(fn):
    with open(fn) as f:
        workflows_s, ratings_s = f.read().split('\n\n')
        workflows = dict([parse_workflow(l) for l in workflows_s.rstrip().split('\n')])
        ratings = [parse_rating(l) for l in ratings_s.rstrip().split('\n')]

        return workflows, ratings

def apply_conditional(rating, conditional):
    match conditional.operator:
        case '<': return rating[conditional.rating] < conditional.value
        case '>': return rating[conditional.rating] > conditional.value
        case _: raise Exception(conditional)

def apply_workflow(rating, workflow):
    for conditional in workflow[0]:
        if apply_conditional(rating, conditional):
            return conditional.target

    return workflow[1]

def replace_noops(rules, noops):
    return [
        [
            Conditional(
                c.rating,
                c.operator,
                c.value,
                noops.get(c.target, c.target)
            )
            for c
            in rules[0]
        ],
        noops.get(rules[1], rules[1])
    ]

def optimize(workflows):
    while True:
        noop_rules = {name: rules[1] for name, rules in workflows.items() if all(c.target == rules[1] for c in rules[0])}
        if not noop_rules:
            break
        workflows = {name: replace_noops(rules, noop_rules) for name, rules in workflows.items() if name not in noop_rules}
    
    return workflows

def apply_conditional_parallel(constraints, conditional):
    active = constraints[conditional.rating]
    match conditional.operator:
        case '<':
            max_if_true = conditional.value - 1
            min_if_false = conditional.value
            true_constraint = Constraint(active.min_value, min(active.max_value, max_if_true))
            false_constraint = Constraint(max(active.min_value, min_if_false), active.max_value)
        case '>':
            min_if_true = conditional.value + 1
            max_if_false = conditional.value
            true_constraint = Constraint(max(active.min_value, min_if_true), active.max_value)
            false_constraint = Constraint(active.min_value, min(active.max_value, max_if_false))
        case _: raise Exception(conditional)

    constraints_true = {k: (true_constraint if k == conditional.rating else v) for k, v in constraints.items()} if true_constraint.range() > 0 else None
    constraints_false = {k: (false_constraint if k == conditional.rating else v) for k, v in constraints.items()} if false_constraint.range() > 0 else None
        
    return constraints_true, constraints_false

def apply_workflow_parallel(workflows, state):
    active_workflow, constraints = state

    states_out = []
    for conditional in workflows[active_workflow][0]:
        constraints_true, constraints_false = apply_conditional_parallel(constraints, conditional)
        if constraints_true is not None:
            states_out.append((conditional.target, constraints_true))
        constraints = constraints_false
        if constraints is None:
            break

    if constraints is not None:
        states_out.append((workflows[active_workflow][1], constraints))

    return states_out

def filter_complete(states):
    filtered = []
    accepted = 0
    for state in states:
        match state[0]:
            case 'A': accepted += functools.reduce(operator.mul, (c.range() for c in state[1].values()))
            case 'R': pass
            case _: filtered.append(state)

    return filtered, accepted

def main():
    workflows, ratings = parse(sys.argv[1])

    workflows = optimize(workflows)

    part1 = 0
    for rating in ratings:
        workflow = 'in'
        while True:
            workflow = apply_workflow(rating, workflows[workflow])
            match workflow:
                case 'A':
                    part1 += sum(rating.values())
                    break
                case 'R': break

    print(part1)

    states = [('in', {k: Constraint(1, 4000) for k in ratings[0].keys()})]
    part2 = 0
    total_states = 1
    while states:
        states = [s for state in states for s in apply_workflow_parallel(workflows, state)]
        total_states += len(states)
        states, accepted = filter_complete(states)
        part2 += accepted

    print(part2, total_states)

if __name__ == '__main__':
    main()
