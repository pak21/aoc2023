#!/usr/bin/env python3

import heapq
import sys

def maybe_add(todo, city, old_location, old_loss, new_direction, new_n_forward):
    new_x = old_location[0] + MOVES[new_direction][0]
    new_y = old_location[1] + MOVES[new_direction][1]
    if new_x < 0 or new_x >= max_x or new_y < 0 or new_y >= max_y:
        return

    new_state = ((new_x, new_y), new_direction, new_n_forward)
    new_loss = old_loss + city[new_y][new_x]

    heapq.heappush(todo, (new_loss, new_state))

max_forward = int(sys.argv[2])
min_turn = int(sys.argv[3])
with open(sys.argv[1]) as f:
    city = [[int(c) for c in row.rstrip()] for row in f.readlines()]

max_x = len(city[0])
max_y = len(city)

todo = [(0, ((0, 0), 0, 0)), (0, ((0, 0), 3, 0))]
seen = set()

MOVES = [(1, 0), (0, -1), (-1, 0), (0, 1)]

target = (max_x - 1, max_y - 1)

while todo:
    loss, state = heapq.heappop(todo)

    if state in seen:
        continue

    seen.add(state)

    location, direction, n_forward = state

    if location == target:
        print(loss)
        break
    else:
        if n_forward >= min_turn:
            maybe_add(todo, city, location, loss, (direction + 1) % 4, 1)
            maybe_add(todo, city, location, loss, (direction - 1) % 4, 1)
        if n_forward < max_forward:
            maybe_add(todo, city, location, loss, direction, n_forward + 1)
