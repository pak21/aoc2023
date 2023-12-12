#!/usr/bin/env python3

import enum
import sys

def debug(*args):
    if debug_on:
        print(*args)

def parse_line(l, repeats):
    springs, result = l.split()
    springs = '?'.join([springs] * repeats)
    result = ','.join([result] * repeats)
    return list(springs), [int(x) for x in result.split(',')]

def score_line(springs):
    in_run = False
    runs = []
    early_exit = False
    for s in springs:
        if s == '?':
            early_exit = True
            break

        match (in_run, s):
            case (False, '.'):
                pass
            case (False, '#'):
                in_run = True
                run_length = 1
            case (True, '.'):
                in_run = False
                runs.append(run_length)
            case (True, '#'):
                run_length += 1
            case _: raise Exception((in_run, s))

    if in_run and not early_exit:
        runs.append(run_length)

    return runs

class Result(enum.Enum):
    FAIL = enum.auto(),
    PASS = enum.auto(),
    INCONCLUSIVE = enum.auto()

def compare(score, result):
    if any(a != b for a, b in zip(score, result)):
        return Result.FAIL

    return (Result.PASS if len(score) == len(result) else Result.INCONCLUSIVE)

def combinations_(springs, result, unknowns):
    idx = unknowns[0]
    good = 0
    evaluations = 0
    for v in ['#', '.']:
        copy = springs[:]
        copy[idx] = v
        score = score_line(copy)
        compared = compare(score, result)
        debug(copy, score, compared)
        evaluations += 1

        match compared:
            case Result.FAIL: pass
            case Result.PASS:
                if len(unknowns) == 1:
                    good += 1
                else:
                    g, e = combinations_(copy, result, unknowns[1:])
                    good += g
                    evaluations += e
            case Result.INCONCLUSIVE:
                if len(unknowns) > 1:
                    g, e = combinations_(copy, result, unknowns[1:])
                    good += g
                    evaluations += e
            case _: raise Exception(compared)

    return good, evaluations

def combinations(springs, result):
    unknowns = [i for i, c in enumerate(springs) if c == '?']

    return combinations_(springs, result, unknowns)

repeats = int(sys.argv[2])
debug_on = int(sys.argv[3])
with open(sys.argv[1]) as f:
    puzzle = [parse_line(l, repeats) for l in f]

output = 0
evals = 0
for springs, result in puzzle:
    g, e = combinations(springs, result)
    print(''.join(springs), g, e)
    output += g
    evals += e

print(output, evals)
