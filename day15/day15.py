import re
from collections import defaultdict


def day15(filename):
    with open(filename, "r") as file:
        data = file.read()

    keys = data.split(",")

    result1 = 0
    for key in keys:
        curr_val = 0
        for c in key:
            curr_val = ((curr_val + ord(c)) * 17) % 256

        result1 += curr_val

    print(f"result1: {result1}")

    boxes = defaultdict(dict)

    for key in keys:
        operator = re.search(r"[=|-]", key)
        box = 0
        for i in range(operator.start()):
            box = ((box + ord(key[i])) * 17) % 256
        item_key = key[: operator.start()]
        if operator.group() == "=":
            boxes[box][item_key] = int(key[operator.start() + 1 :])
        else:
            boxes[box].pop(item_key, None)

    result2 = 0
    for key, value in boxes.items():
        for ind, item in enumerate(value.values()):
            result2 += (key + 1) * (ind + 1) * item

    print(f"result2: {result2}")


day15("sample.txt")
day15("input.txt")
