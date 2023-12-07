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

ORDERING_JOKERS = {
    'T': 'a',
    'Q': 'c',
    'K': 'd',
    'A': 'e',

    'J': '0',
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

def parse(l):
    cards, bid = l.split()
    return cards, int(bid)

def parse_hand(c):
    return HAND_RANKS[tuple(sorted(collections.Counter((collections.Counter(c).values())).items()))]

def key_no_jokers(cards):
    return (
        parse_hand(cards),
        [ORDERING.get(c, c) for c in cards]
    )

def key_with_jokers(cards):
    return (
        max(parse_hand(cards.replace('J', joker)) for joker in JOKER_CARDS),
        [ORDERING_JOKERS.get(c, c) for c in cards]
    )

with open(sys.argv[1]) as f:
    data = [parse(l) for l in f.readlines()]

parts = (
    sum(
        i * bid
        for i, (_, bid)
        in enumerate(
            sorted(
                (fn(cards), bid)
                for cards, bid
                in data
            ),
        1)
    )
    for fn
    in [key_no_jokers, key_with_jokers]
)

for part in parts:
    print(part)
