#!/usr/bin/env python3

import collections
import functools
import sys

def parse_line(l, repeats):
    springs, result = l.split()
    springs = '?'.join([springs] * repeats)
    result = ','.join([result] * repeats)
    return springs, tuple(int(x) for x in result.split(','))

def is_sublist(needle, haystack):
    length = len(needle)
    return any(needle == haystack[base:base+length] for base in range(len(haystack)-length+1))

def key_filter(k, filter_params):
    is_run, before, middle, after = k
    longest, result = filter_params
    match is_run:
        case False:
            if before > longest or after > longest:
                return False

            return is_sublist(list(middle), list(result))
        case True: return before <= longest

def combine_with_dot(before, after):
    before_is_run, before_l, before_m, before_r = before
    after_is_run, after_l, after_m, after_r = after

    match (before_is_run, after_is_run):
        case (False, False):
            match (before_r > 0, after_l > 0):
                case (False, False): return (False, before_l, (*before_m, *after_m), after_r)
                case (False, True): return (False, before_l, (*before_m, after_l, *after_m), after_r)
                case (True, False): return (False, before_l, (*before_m, before_r, *after_m), after_r)
                case (True, True): return (False, before_l, (*before_m, before_r, after_l, *after_m), after_r)
        case (False, True):
            match before_r > 0:
                case False: return (False, before_l, before_m, after_l)
                case True: return (False, before_l, (*before_m, before_r), after_l)
        case (True, False):
            match after_l > 0:
                case False: return (False, before_l, after_m, after_r)
                case True: return (False, before_l, (after_l, *after_m), after_r)
        case (True, True): return (False, before_l, (), after_l)

def remove_dot(before, after, filter_params):
    before_p = get_possibilities(before, filter_params)
    after_p = get_possibilities(after, filter_params)

    r = collections.defaultdict(int)
    for before, before_count in before_p.items():
        for after, after_count in after_p.items():
            k = combine_with_dot(before, after)
            if key_filter(k, filter_params):
                r[k] += before_count * after_count 

    return r

def combine_with_hash(before, after):
    before_is_run, before_l, before_m, before_r = before
    after_is_run, after_l, after_m, after_r = after

    match (before_is_run, after_is_run):
        case (False, False): return (False, before_l, (*before_m, before_r + 1 + after_l, *after_m), after_r)
        case (False, True): return (False, before_l, before_m, before_r + 1 + after_l)
        case (True, False): return (False, before_l + 1 + after_l, after_m, after_r)
        case (True, True): return (True, before_l + 1 + after_l, None, None)

def remove_hash(before, after, filter_params):
    before_p = get_possibilities(before, filter_params)
    after_p = get_possibilities(after, filter_params)

    r = collections.defaultdict(int)
    for before, before_count in before_p.items():
        for after, after_count in after_p.items():
            k = combine_with_hash(before, after)
            if key_filter(k, filter_params):
                r[k] += before_count * after_count 

    return r

def remove_question(before, after, filter_params):
    with_dot = remove_dot(before, after, filter_params)
    with_hash = remove_hash(before, after, filter_params)

    for k, v in with_hash.items():
        if k in with_dot:
            with_dot[k] += v
        else:
            with_dot[k] = v

    return with_dot

@functools.cache
def get_possibilities(springs, filter_params):
    if springs == '':
        return {(True, 0, None, None): 1}

    split_point = len(springs) // 2
    match springs[split_point]:
        case '.': return remove_dot(springs[:split_point], springs[split_point+1:], filter_params)
        case '#': return remove_hash(springs[:split_point], springs[split_point+1:], filter_params)
        case '?': return remove_question(springs[:split_point], springs[split_point+1:], filter_params)

repeats = int(sys.argv[2])
with open(sys.argv[1]) as f:
    puzzle = [parse_line(l, repeats) for l in f]

answer = 0
for springs, result in puzzle:

    filter_params = (max(result), result)
    possibilities = get_possibilities(springs, filter_params)

    n = 0
    for (is_run, before, middle, after), count in possibilities.items():
        match is_run:
            case False:
                match (before > 0, after > 0):
                    case (False, False): k = middle
                    case (False, True): k = (*middle, after)
                    case (True, False): k = (before, *middle)
                    case (True, True): k = (before, *middle, after)
            case True: k = (before,)

        if k == result:
            n += count

    answer += n
    print(springs, result, n)

print(answer)
