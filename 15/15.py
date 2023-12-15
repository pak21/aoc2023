#!/usr/bin/env python3

import collections
import sys

def hash_fn(s):
    v = 0
    for c in s:
        v = (17 * (v + ord(c))) % 256
    
    return v

with open(sys.argv[1]) as f:
   steps = f.readline().rstrip().split(',')

print(sum((hash_fn(step) for step in steps)))

boxes = collections.defaultdict(list)

for step in steps:
    if step[-1] == '-':
        label = step[:-1]
        box = hash_fn(label)

        to_remove = None
        for i, (old_label, _) in enumerate(boxes[box]):
            if label == old_label:
                to_remove = i
                break

        if to_remove is not None:
            del boxes[box][to_remove]
    else:
        label, focal = step.split('=')
        box = hash_fn(label)
        focal = int(focal)

        found = False
        for i, (old_label, old_focal) in enumerate(boxes[box]):
            if label == old_label:
                boxes[box][i] = (label, focal)
                found = True
                break

        if not found:
            boxes[box].append((label, focal))

print(sum((box + 1) * (i + 1) * focal for box, lenses in boxes.items() for i, (_, focal) in enumerate(lenses)))
