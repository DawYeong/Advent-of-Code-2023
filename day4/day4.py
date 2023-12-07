import math
from collections import defaultdict


def day4(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    result1 = 0

    cards = defaultdict(int, {k: 1 for k in range(len(lines))})

    for line in lines:
        split = list(filter(lambda x: len(x) != 0, line.split(" ")))[1:]
        card_number = int(split[0][:-1]) - 1
        sep = split.index("|")
        winning = set(split[1:sep])
        card_numbers = set(split[sep + 1 :])
        matches = winning.intersection(card_numbers)
        result1 += int(math.pow(2, len(matches) - 1)) if len(matches) != 0 else 0

        for i in range(len(matches)):
            cards[card_number + i + 1] += cards[card_number]

    print(f"result1: {result1}")
    print(f"result2: {sum(cards.values())}")


day4("sample.txt")
day4("input.txt")
