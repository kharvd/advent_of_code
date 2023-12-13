from collections import Counter
import sys


CARD_VALUES = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,  # 10
    "Q": 12,  # Queen
    "K": 13,  # King
    "A": 14,  # Ace
}

HAND_TYPES = {
    "HIGH_CARD": 0,
    "ONE_PAIR": 1,
    "TWO_PAIR": 2,
    "THREE_OF_A_KIND": 3,
    "FULL_HOUSE": 4,
    "FOUR_OF_A_KIND": 5,
    "FIVE_OF_A_KIND": 6,
}


def decode_hand(hand):
    return tuple(CARD_VALUES[h] for h in hand)


def get_hand_type(hand):
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    num_jokers = counts.get(CARD_VALUES["J"], 0)

    count_values = Counter()
    for card, count in counts.items():
        count_values[count] += 1

    if count_values[5] == 1:
        return HAND_TYPES["FIVE_OF_A_KIND"]
    elif count_values[4] == 1:
        if num_jokers > 0:
            return HAND_TYPES["FIVE_OF_A_KIND"]
        return HAND_TYPES["FOUR_OF_A_KIND"]
    elif count_values[3] == 1 and count_values[2] == 1:
        if num_jokers > 0:
            return HAND_TYPES["FIVE_OF_A_KIND"]
        return HAND_TYPES["FULL_HOUSE"]
    elif count_values[3] == 1:
        if num_jokers > 0:
            return HAND_TYPES["FOUR_OF_A_KIND"]
        return HAND_TYPES["THREE_OF_A_KIND"]
    elif count_values[2] == 2:
        if num_jokers == 2:
            return HAND_TYPES["FOUR_OF_A_KIND"]
        if num_jokers == 1:
            return HAND_TYPES["FULL_HOUSE"]
        return HAND_TYPES["TWO_PAIR"]
    elif count_values[2] == 1:
        if num_jokers > 0:
            return HAND_TYPES["THREE_OF_A_KIND"]
        return HAND_TYPES["ONE_PAIR"]
    else:
        if num_jokers > 0:
            return HAND_TYPES["ONE_PAIR"]
        return HAND_TYPES["HIGH_CARD"]


def read_hand(s):
    hand, bid = s.split(" ")
    return decode_hand(hand), int(bid), s


hands = [read_hand(line) for line in sys.stdin.readlines()]

hands.sort(key=lambda x: (get_hand_type(x[0]), x[0]))

winnings = 0
for rank, hands in enumerate(hands):
    winnings += (rank + 1) * hands[1]

print(winnings)
