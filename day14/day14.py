import copy
import numpy as np

lines = []


def day14(filename):
    with open(filename, "r") as file:
        data = file.read()
    global lines
    lines = [list(line) for line in data.split("\n")]
    length = len(lines[0])

    def tilt():
        states = []
        for i in range(length):
            curr_state = []
            for j in range(len(lines)):
                if lines[j][i] == ".":
                    continue
                elif lines[j][i] == "#":
                    curr_state.append((j, lines[j][i]))
                else:
                    lines[j][i] = "."
                    if len(curr_state) == 0:
                        lines[0][i] = "O"
                        curr_state.append((0, lines[j][i]))
                    else:
                        lines[curr_state[len(curr_state) - 1][0] + 1][i] = "O"
                        curr_state.append(
                            (curr_state[len(curr_state) - 1][0] + 1, lines[j][i])
                        )

            states.append(curr_state)

        return states

    def cycle():
        global lines
        # saving north for part1
        north_tilt = tilt()
        lines = np.rot90(lines, k=1, axes=(1, 0))
        tilt()
        lines = np.rot90(lines, k=1, axes=(1, 0))
        tilt()
        lines = np.rot90(lines, k=1, axes=(1, 0))
        tilt()
        lines = np.rot90(lines, k=1, axes=(1, 0))

        return north_tilt

    result1 = 0
    north = cycle()
    for state in north:
        for s in state:
            if s[1] == "#":
                continue
            result1 += length - s[0]

    print(f"result1: {result1}")

    cycle_states = [copy.deepcopy(lines)]
    raw_states = [",".join(["".join(line) for line in lines])]

    cycle_start = 0
    count = 1

    while True:
        cycle()
        # when adding to list, we need to add a deepcopy or else every item will be the same because the reference is the same
        lines_copy = copy.deepcopy(lines)
        new_state = ",".join(["".join(line) for line in lines])
        if new_state in raw_states:
            cycle_start = raw_states.index(new_state)
            break
        else:
            cycle_states.append(lines_copy)
            raw_states.append(new_state)

        count += 1

    billionth_state = cycle_states[
        (1000000000 - cycle_start) % (len(cycle_states) - cycle_start) + cycle_start - 1
    ]

    result2 = 0
    for i, line in enumerate(billionth_state):
        result2 += (length - i) * len([c for c in line if c == "O"])

    print(f"result2: {result2}")


day14("sample.txt")
day14("input.txt")
