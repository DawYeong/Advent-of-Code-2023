DIRECTION = {
    0: (0, 1),  # right
    1: (1, 0),  # down
    2: (0, -1),  # left
    3: (-1, 0),  # up
}


def dfs(lines, start):
    work_list = [(start[0], start[1], start[2])]
    seen = set()

    while work_list:
        item = work_list.pop()

        if item in seen:
            continue

        seen.add(item)

        dir = DIRECTION[item[2]]
        next_location = (item[0] + dir[0], item[1] + dir[1])

        if (
            next_location[0] < 0
            or next_location[0] >= len(lines)
            or next_location[1] < 0
            or next_location[1] >= len(lines[0])
        ):
            continue

        next_symbol = lines[next_location[0]][next_location[1]]

        if next_symbol == "\\":
            work_list.append(
                (
                    next_location[0],
                    next_location[1],
                    (item[2] + 1) % 4 if item[2] % 2 == 0 else (item[2] - 1) % 4,
                )
            )
        elif next_symbol == "/":
            work_list.append(
                (
                    next_location[0],
                    next_location[1],
                    (item[2] + 1) % 4 if item[2] % 2 == 1 else (item[2] - 1) % 4,
                )
            )
        elif next_symbol == "-":
            if item[2] % 2 == 1:
                work_list.append((next_location[0], next_location[1], 0))
                work_list.append((next_location[0], next_location[1], 2))
            else:
                work_list.append((next_location[0], next_location[1], item[2]))
        elif next_symbol == "|":
            if item[2] % 2 == 0:
                work_list.append((next_location[0], next_location[1], 1))
                work_list.append((next_location[0], next_location[1], 3))
            else:
                work_list.append((next_location[0], next_location[1], item[2]))
        else:
            # empty space
            work_list.append((next_location[0], next_location[1], item[2]))

    energized = set()
    for item in seen:
        energized.add((item[0], item[1]))

    result = len(energized) - 1

    return result


def day16(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    result1 = dfs(lines, (0, -1, 0))
    print(f"result1: {result1}")

    # running dfs on all possible starting positions...
    result2 = 0
    for i in range(len(lines)):
        result2 = max(
            result2, dfs(lines, (i, -1, 0)), dfs(lines, (i, len(lines[0]), 2))
        )

    for j in range(len(lines[0])):
        result2 = max(result2, dfs(lines, (-1, j, 1)), dfs(lines, (len(lines), j, 3)))

    print(f"result2: {result2}")


day16("sample.txt")
day16("input.txt")
