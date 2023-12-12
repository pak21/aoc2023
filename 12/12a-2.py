#!/usr/bin/env python3

import enum
import sys

def parse_line(l):
    springs, result = l.split()
    springs = '?'.join([springs] * 5)
    result = ','.join([result] * 5)
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
    for v in ['#', '.']:
        copy = springs[:]
        copy[idx] = v
        score = score_line(copy)
        compared = compare(score, result)
#        print(copy, score, compared)

        match compared:
            case Result.FAIL: pass
            case Result.PASS:
                if len(unknowns) == 1:
                    good += 1
                else:
                    good += combinations_(copy, result, unknowns[1:])
            case Result.INCONCLUSIVE:
                if len(unknowns) > 1:
                    good += combinations_(copy, result, unknowns[1:])
            case _: raise Exception(compared)

    return good

def combinations(springs, result):
    unknowns = [i for i, c in enumerate(springs) if c == '?']

    return combinations_(springs, result, unknowns)

with open(sys.argv[1]) as f:
    puzzle = [parse_line(l) for l in f]

if True:
    part1 = 0
    for springs, result in puzzle:
        r = combinations(springs, result)
        print(''.join(springs), r)
        part1 += r

    print(part1)
