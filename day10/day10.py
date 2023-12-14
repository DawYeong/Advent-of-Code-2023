# (x, y)
# +x: south, -x: north, +y: east, -y: west

DIRECTIONS = {
    "S": [(1, 0), (-1, 0), (0, 1), (0, -1)],  # start
    "|": [(1, 0), (-1, 0)],  # connects north and south
    "-": [(0, 1), (0, -1)],  # connects west and east
    "L": [(-1, 0), (0, 1)],  # connects north and east
    "J": [(-1, 0), (0, -1)],  # connects north and west
    "7": [(1, 0), (0, -1)],  # connects south and west
    "F": [(1, 0), (0, 1)],  # connects south and east
}


def day10(filename):
    print(f"Filename: {filename}")
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")
    width = len(lines[0])
    length = len(lines)

    # find starting pos => run dfs => since it's one cycle, capture the length of the cycle and divide by 2
    start = data.replace("\n", "").index("S")
    work_list = [(start // width, start % width, 1)]

    visited = set()
    nodes = []
    time = 0
    while work_list:
        item = work_list.pop()

        time = max(time, item[2])

        visited.add((item[0], item[1]))
        nodes.append((item[0], item[1]))
        new_dirs = DIRECTIONS[lines[item[0]][item[1]]]

        for dir in new_dirs:
            new_item = (item[0] + dir[0], item[1] + dir[1], item[2] + 1)
            if (
                (new_item[0], new_item[1]) in visited
                or new_item[0] < 0
                or new_item[0] >= length
                or new_item[1] < 0
                or new_item[1] >= width
                or lines[new_item[0]][new_item[1]] == "."
            ):
                continue

            # at the start we can't just traverse any node => has to make sense with the direction
            if lines[item[0]][item[1]] == "S" and not (
                (
                    dir[0] == 1
                    and (
                        lines[new_item[0]][new_item[1]] == "L"
                        or lines[new_item[0]][new_item[1]] == "|"
                        or lines[new_item[0]][new_item[1]] == "J"
                    )
                )
                or (
                    dir[0] == -1
                    and (
                        lines[new_item[0]][new_item[1]] == "7"
                        or lines[new_item[0]][new_item[1]] == "|"
                        or lines[new_item[0]][new_item[1]] == "F"
                    )
                )
                or (
                    dir[1] == 1
                    and (
                        lines[new_item[0]][new_item[1]] == "J"
                        or lines[new_item[0]][new_item[1]] == "-"
                        or lines[new_item[0]][new_item[1]] == "7"
                    )
                )
                or (
                    dir[1] == -1
                    and (
                        lines[new_item[0]][new_item[1]] == "L"
                        or lines[new_item[0]][new_item[1]] == "-"
                        or lines[new_item[0]][new_item[1]] == "F"
                    )
                )
            ):
                continue

            work_list.append(new_item)

    # using shoelace formula to calculate the inner area
    det = 0
    for i in range(len(nodes)):
        det += (
            nodes[i][0] * nodes[(i + 1) % len(nodes)][1]
            - nodes[(i + 1) % len(nodes)][0] * nodes[i][1]
        )

    # because the edges are 1 character wide, we use this formula to get the result
    result2 = abs(det) // 2 - (len(nodes) - 1) // 2 + 1
    print(f"result1: {time//2}")
    print(f"result2: {result2}")


day10("sample1.txt")
day10("sample2.txt")
day10("sample3.txt")
day10("input.txt")
