#!/usr/bin/env python3

import collections
import sys

ORDERING = {
    'T': 'a',
    'J': 'b',
    'Q': 'c',
    'K': 'd',
    'A': 'e'
}

JOKER_CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

HAND_RANKS = {
    ((5, 1),): 6, # Five of a kind
    ((1, 1), (4, 1)): 5, # Four of a kind
    ((2, 1), (3, 1)): 4, # Full house
    ((1, 2), (3, 1)): 3, # Three of a kind
    ((1, 1), (2, 2)): 2, # Two pair
    ((1, 3), (2, 1)): 1, # One pair
    ((1, 5),): 0 # High card
}

def parse(line):
    cards, bid = line.split()
    return cards, int(bid)

def rank_hand(cards):
    return HAND_RANKS[tuple(sorted(collections.Counter((collections.Counter(cards).values())).items()))]

def key_no_jokers(cards):
    return (rank_hand(cards), [ORDERING.get(c, c) for c in cards])

def key_with_jokers(cards):
    return (
        max(rank_hand(cards.replace('J', joker)) for joker in JOKER_CARDS),
        ['0' if c == 'J' else ORDERING.get(c, c) for c in cards]
    )

with open(sys.argv[1]) as f:
    data = [parse(l) for l in f.readlines()]

parts = (
    sum(
        i * bid
        for i, (_, bid)
        in enumerate(sorted(data, key=lambda d: fn(d[0])), 1)
    )
    for fn
    in [key_no_jokers, key_with_jokers]
)

for part in parts:
    print(part)
