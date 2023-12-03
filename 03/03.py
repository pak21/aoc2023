#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

numbers = {}
symbols = {}

for y in range(0, len(lines)):
    l = lines[y].rstrip()
    x = 0
    current_number = None
    for x in range(0, len(l)):
        c = l[x]
        if c.isdigit():
            if current_number is None:
                current_number = int(c)
                current_number_start = (x, y)
                current_number_length = 1
            else:
                current_number = current_number * 10 + int(c)
                current_number_length += 1
        else:
            if current_number is not None:
                numbers[current_number_start] = (current_number, current_number_length, False)
                current_number = None

            if c != '.':
                symbols[(x, y)] = c

    if current_number is not None:
        numbers[current_number_start] = (current_number, current_number_length, False)

number_pointers = {}
for (x0, y), (_, l, _) in numbers.items():
    for x in range(x0, x0 + l):
        number_pointers[(x, y)] = (x0, y) 

part1 = 0
part2 = 0

for (sx, sy), s in symbols.items():
    adjacent = 0
    ratio = 1
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x = sx + dx
            y = sy + dy
            pointer = number_pointers.get((x, y))
            if pointer is not None:
                target = numbers[pointer]
                if not target[2]:
                    adjacent += 1
                    part1 += target[0]
                    ratio *= target[0]
                    numbers[pointer] = (target[0], target[1], True)

    if s == '*' and adjacent == 2:
        part2 += ratio

print(part1)
print(part2)
