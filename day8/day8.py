import re
import copy
import math


def day8(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = list(filter(lambda x: len(x) != 0, data.split("\n")))
    directions = [0 if x == "L" else 1 for x in lines[0]]

    paths = {}

    for i in range(1, len(lines)):
        nodes = re.findall(r"[0-9A-Z]+", lines[i])
        paths[nodes[0]] = [nodes[1], nodes[2]]

    destination = "AAA"
    result1 = 0
    while destination != "ZZZ" and destination in paths:
        prev_destination = destination
        destination = paths[prev_destination][directions[result1 % len(directions)]]
        if prev_destination == destination:
            print("cant find path")
            break
        result1 += 1

    print(f"result1: {result1}")
    starting_pos = list(filter(lambda x: x[2] == "A", paths.keys()))

    num_nodes = len(starting_pos)
    times = []
    curr_pos = copy.deepcopy(starting_pos)

    for i in range(num_nodes):
        time = 0
        while curr_pos[i][2] != "Z":
            curr_pos[i] = paths[curr_pos[i]][directions[time % len(directions)]]
            time += 1

        times.append(time)

    # doing it this way because of version of python
    # in 3.9, you can do math.lcm()
    result2 = 1
    for i in times:
        result2 = result2 * i // math.gcd(result2, i)
    print(f"result2: {result2}")


# day8("sample1.txt")
# day8("sample2.txt")
day8("sample3.txt")
day8("input.txt")
