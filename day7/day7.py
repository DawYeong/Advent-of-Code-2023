from collections import Counter

VALUE_MAP1 = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}
VALUE_MAP2 = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 0,
    "Q": 11,
    "K": 12,
    "A": 13,
}

COMBOS = {
    "high": 1,
    "1pair": 2,
    "2pair": 3,
    "trips": 4,
    "fullhouse": 5,
    "quads": 6,
    "five": 7,
}


def add_to_combo(card_combos, count, combo):
    if count[0][1] == 5:
        card_combos["five"].append(combo)
    elif count[0][1] == 4:
        card_combos["quads"].append(combo)
    elif count[0][1] == 3:
        if count[1][1] == 2:
            card_combos["fullhouse"].append(combo)
        else:
            card_combos["trips"].append(combo)
    elif count[0][1] == 2:
        if count[1][1] == 2:
            card_combos["2pair"].append(combo)
        else:
            card_combos["1pair"].append(combo)
    else:
        card_combos["high"].append(combo)


def day7(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    # assuming there are no duplicate hands
    bets = {}
    card_combos1 = {
        "high": [],
        "1pair": [],
        "2pair": [],
        "trips": [],
        "fullhouse": [],
        "quads": [],
        "five": [],
    }
    card_combos2 = {
        "high": [],
        "1pair": [],
        "2pair": [],
        "trips": [],
        "fullhouse": [],
        "quads": [],
        "five": [],
    }

    for line in lines:
        split = line.split(" ")
        bets[split[0]] = int(split[1])
        count = Counter(split[0])

        top1 = count.most_common()
        add_to_combo(card_combos1, top1, split[0])

        if count["J"] and count["J"] != 5:
            j_count = count["J"]
            del count["J"]
            top1 = count.most_common()
            top1[0] = (top1[0][0], top1[0][1] + j_count)

        add_to_combo(card_combos2, top1, split[0])

    ordered_combos1 = []
    for v in card_combos1.values():
        v.sort(
            key=lambda x: (
                VALUE_MAP1[x[0]],
                VALUE_MAP1[x[1]],
                VALUE_MAP1[x[2]],
                VALUE_MAP1[x[3]],
                VALUE_MAP1[x[4]],
            )
        )
        ordered_combos1.extend(v)

    ordered_combos2 = []
    for v in card_combos2.values():
        v.sort(
            key=lambda x: (
                VALUE_MAP2[x[0]],
                VALUE_MAP2[x[1]],
                VALUE_MAP2[x[2]],
                VALUE_MAP2[x[3]],
                VALUE_MAP2[x[4]],
            )
        )
        ordered_combos2.extend(v)

    result1 = 0
    result2 = 0
    for i in range(len(ordered_combos1)):
        result1 += (i + 1) * bets[ordered_combos1[i]]
        result2 += (i + 1) * bets[ordered_combos2[i]]

    print(f"result1: {result1}")
    print(f"result2: {result2}")


day7("sample.txt")
day7("input.txt")
