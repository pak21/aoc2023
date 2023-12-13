#!/usr/bin/env python3

import collections
import functools
import sys

def debug(*args):
    if debug_on:
        print(*args)

def parse_line(l, repeats):
    springs, result = l.split()
    springs = '?'.join([springs] * repeats)
    result = ','.join([result] * repeats)
    return springs, tuple([int(x) for x in result.split(',')])

evals = 0

def is_sublist(needle, haystack):
    length = len(needle)
    return any(needle == haystack[base:base+length] for base in range(len(haystack)-length+1))

def key_filter(k, filter_params):
    is_run, before, middle, after = k
    longest, max_runs, result = filter_params
    match is_run:
        case False:
            if before > longest or after > longest:
                return False
            n_runs = len(middle) + sum([before > 0, after > 0])
            if n_runs > max_runs:
                return False

            if not is_sublist(list(middle), list(result)):
                return False

            return True
        case True: return before <= longest

def remove_dot(before, after, filter_params):
    debug('remove_dot', before, after)
    before_p = get_possibilities(before, filter_params)
    after_p = get_possibilities(after, filter_params)

    r = collections.defaultdict(int)
    for (before_is_run, before_l, before_m, before_r), before_count in before_p.items():
        for (after_is_run, after_l, after_m, after_r), after_count in after_p.items():
            match (before_is_run, after_is_run):
                case (False, False):
                    match (before_r > 0, after_l > 0):
                        case (False, False): k = (False, before_l, (*before_m, *after_m), after_r)
                        case (False, True): k = (False, before_l, (*before_m, after_l, *after_m), after_r)
                        case (True, False): k = (False, before_l, (*before_m, before_r, *after_m), after_r)
                        case (True, True): k = (False, before_l, (*before_m, before_r, after_l, *after_m), after_r)
                case (False, True):
                    match before_r > 0:
                        case False: k = (False, before_l, before_m, after_l)
                        case True: k = (False, before_l, (*before_m, before_r), after_l)
                case (True, False):
                    match after_l > 0:
                        case False: k = (False, before_l, after_m, after_r)
                        case True: k = (False, before_l, (after_l, *after_m), after_r)
                case (True, True):
                    k = (False, before_l, (), after_l)

            r[k] += before_count * after_count 
    return r

def remove_hash(before, after, filter_params):
    debug('remove_hash', before, after)
    before_p = get_possibilities(before, filter_params)
    after_p = get_possibilities(after, filter_params)

    r = collections.defaultdict(int)
    for (before_is_run, before_l, before_m, before_r), before_count in before_p.items():
        for (after_is_run, after_l, after_m, after_r), after_count in after_p.items():
            match (before_is_run, after_is_run):
                case (False, False):
                    k = (False, before_l, (*before_m, before_r + 1 + after_l, *after_m), after_r)
                case (False, True):
                    k = (False, before_l, before_m, before_r + 1 + after_l)
                case (True, False):
                    k = (False, before_l + 1 + after_l, after_m, after_r)
                case (True, True):
                    k = (True, before_l + 1 + after_l, None, None)

            if key_filter(k, filter_params):
                r[k] += before_count * after_count 

    return r

def remove_question(before, after, filter_params):
    debug('remove_question', before, after)

    with_dot = get_possibilities(before + '.' + after, filter_params)
    with_hash = get_possibilities(before + '#' + after, filter_params)

    r = collections.defaultdict(int, with_dot)
    for k, v in with_hash.items():
        r[k] += v

    return r

@functools.cache
def get_possibilities(big, filter_params):
    global evals
    debug('start get_possibilities', big)

    match big:
        case '':
            r = {(True, 0, None, None): 1}
            debug('get_possibilities', big, r)
            return r
        case '#':
            r = {(True, 1, None, None): 1}
            debug('get_possibilities', big, r)
            return r

    split_point = len(big) // 2
    match big[split_point]:
        case '.':
            r = remove_dot(big[:split_point], big[split_point+1:], filter_params)
        case '#':
            r = remove_hash(big[:split_point], big[split_point+1:], filter_params)
        case '?':
            r = remove_question(big[:split_point], big[split_point+1:], filter_params)
        case _:
            raise Exception(big, split_point, big[split_point])

    evals += len(r)

    debug('get_possibilities', big, len(r))
    return r

repeats = int(sys.argv[2])
debug_on = int(sys.argv[3])
with open(sys.argv[1]) as f:
    puzzle = [parse_line(l, repeats) for l in f]

part1 = 0
for springs, result in puzzle:
    filter_params = (max(result), len(result), result)
    possibilities = get_possibilities(springs, filter_params)
    simplified = collections.defaultdict(int)
    for (is_run, before, middle, after), count in possibilities.items():
        match is_run:
            case False:
                match (before > 0, after > 0):
                    case (False, False): k = middle
                    case (False, True): k = (*middle, after)
                    case (True, False): k = (before, *middle)
                    case (True, True): k = (before, *middle, after)
            case True:
                k = (before,)
        simplified[k] += count
    part1 += simplified[result]
    print(springs, result, simplified[result])

print(part1)
print(evals)
