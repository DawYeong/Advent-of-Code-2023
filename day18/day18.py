DIRECTION = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


def day18(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    directions = list(DIRECTION.values())
    for p2 in [False, True]:
        curr_pos = (0, 0)
        endpoints = []
        perimeter = 0
        for line in lines:
            line_split = line.split(" ")
            if not p2:
                length = int(line_split[1])
                curr_pos = (
                    curr_pos[0] + DIRECTION[line_split[0]][0] * (length),
                    curr_pos[1] + DIRECTION[line_split[0]][1] * (length),
                )
            else:
                length = int(line_split[2][2 : len(line_split[2]) - 2], 16)
                dir = int(line_split[2][len(line_split[2]) - 2])
                curr_pos = (
                    curr_pos[0] + directions[dir][0] * (length),
                    curr_pos[1] + directions[dir][1] * (length),
                )

            endpoints.append(curr_pos)
            perimeter += length

        # use both shoelace formula and pick's theorem
        det = 0
        for i in range(len(endpoints)):
            det += (
                endpoints[i][0] * endpoints[(i + 1) % len(endpoints)][1]
                - endpoints[(i + 1) % len(endpoints)][0] * endpoints[i][1]
            )

        area = abs(det) // 2

        lattice_points = area + 1 - (perimeter // 2)

        result = perimeter + lattice_points

        print(f"result{1 if not p2 else 2}: {result}")


day18("sample.txt")
day18("input.txt")
