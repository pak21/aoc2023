#!/usr/bin/env python3

import sys

NUMBERS = {str(i): i for i in range(1, 10)}

WORDS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def calibration(s, words):
    first_index = len(s) + 1
    last_index = -1
    for a, b in words.items():
        idx = s.find(a)
        if idx != -1 and idx < first_index:
            first_index = idx
            first = b
        idx = s.rfind(a)
        if idx != -1 and idx > last_index:
            last_index = idx
            last = b

    return 10 * first + last

with open(sys.argv[1]) as f:
    lines = f.readlines()

print(sum((calibration(s, NUMBERS) for s in lines)))
print(sum((calibration(s, {**NUMBERS, **WORDS}) for s in lines)))
