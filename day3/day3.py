import re
from collections import defaultdict

PATTERN = r"[^a-zA-Z0-9.]"
NUMBER_PATTERN = r"[0-9]+"


def day3(filename):
    with open(filename, "r") as file:
        data = file.read()

    width = data.find("\n") + 1
    raw_data = data.replace("\n", ".")

    find_symbols = [(m.group(0), m.start()) for m in re.finditer(PATTERN, raw_data)]
    find_numbers = [
        (m.group(0), m.start()) for m in re.finditer(NUMBER_PATTERN, raw_data)
    ]

    result1 = 0
    result2 = 0
    gears = defaultdict(list)
    for num, ind in find_numbers:
        symbol_match = list(
            filter(
                lambda x: (
                    ind - width - 1 <= x[1] <= ind - width + len(num)
                    or x[1] == ind - 1
                    or x[1] == ind + len(num)
                    or ind + width - 1 <= x[1] <= ind + width + len(num)
                ),
                find_symbols,
            )
        )
        if symbol_match:
            if symbol_match[0][0] == "*":
                # this assumes that number is only adjacent to at most one symbol
                gears[symbol_match[0][1]].append(int(num))
            result1 += int(num)

    for v in gears.values():
        if len(v) == 2:
            result2 += v[0] * v[1]

    print(f"result1: {result1}")
    print(f"result2: {result2}")


day3("sample.txt")
day3("input.txt")
