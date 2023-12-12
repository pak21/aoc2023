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
    INCONCLUSIVE = enum.auto(),

    ABORT_MAX = enum.auto(),
    ABORT_SUM = enum.auto(),

def compare(score, result, unknowns_remaining):
    if score and max(score) > max(result):
        return Result.ABORT_MAX

    if sum(score) > sum(result):
        return Result.ABORT_SUM

    if any(a != b for a, b in zip(score, result)):
        return Result.FAIL

    if len(score) == len(result):
        if unknowns_remaining == 0:
            return Result.PASS
        else:
            return Result.INCONCLUSIVE

    if unknowns_remaining == 0:
        return Result.FAIL

    return Result.INCONCLUSIVE

def combinations_(springs, result, unknowns, depth):
    idx = unknowns[0]
    good = 0
    evaluations = 0
    for v in ['.', '#']:
        copy = springs[:]
        copy[idx] = v
        score = score_line(copy)
        compared = compare(score, result, len(unknowns)-1)
        debug(depth, copy, score, compared)
        evaluations += 1

        match compared:
            case Result.ABORT_MAX: break
            case Result.ABORT_SUM: break
            case Result.FAIL: pass
            case Result.PASS: good += 1
            case Result.INCONCLUSIVE:
                g, e = combinations_(copy, result, unknowns[1:], depth+1)
                good += g
                evaluations += e
            case _: raise Exception(compared)

    return good, evaluations

def combinations(springs, result):
    unknowns = [i for i, c in enumerate(springs) if c == '?']

    return combinations_(springs, result, unknowns, 0)

repeats = int(sys.argv[2])
debug_on = int(sys.argv[3])
with open(sys.argv[1]) as f:
    puzzle = [parse_line(l, repeats) for l in f]

output = 0
evals = 0
for springs, result in puzzle:
    g, e = combinations(springs, result)
    print(''.join(springs), g)
    output += g
    evals += e

print(output, evals)
