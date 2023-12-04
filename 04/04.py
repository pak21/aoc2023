#!/usr/bin/env python3

import sys

def parse_card(l):
    prefix, numbers = l.split(': ')
    _, id_s = prefix.split()
    winners_s, card_s = numbers.split(' | ')
    winners = {int(n) for n in winners_s.split()}
    card = {int(n) for n in card_s.split()}
    winner_count = len(winners.intersection(card))
    return int(id_s), winner_count

with open(sys.argv[1]) as f:
    cards = {a: b for a, b in [parse_card(l.rstrip()) for l in f.readlines()]}

print(sum([2**(x-1) for x in cards.values() if x]))

card_counts = {x: 1 for x in cards}

for a, b in card_counts.items():
    winners = cards[a]
    for x in range(a+1, a+winners+1):
        card_counts[x] += b

print(sum(card_counts.values()))
