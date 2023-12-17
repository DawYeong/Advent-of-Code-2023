DP = {}


def traverse(spring_cond, damaged_springs, a, b, length):
    dp_key = (a, b, length)
    if dp_key in DP:
        return DP[dp_key]

    if a == len(spring_cond):
        # end condition
        if b == len(damaged_springs) and length == 0:
            return 1
        elif b == len(damaged_springs) - 1 and length == damaged_springs[b]:
            return 1
        else:
            return 0

    count = 0

    # to prevent duplication
    for char in [".", "#"]:
        if spring_cond[a] == char or spring_cond[a] == "?":
            if char == ".":
                if length == 0:
                    # no blocks continue to the next character
                    count += traverse(spring_cond, damaged_springs, a + 1, b, 0)
                elif b < len(damaged_springs) and length == damaged_springs[b]:
                    # completed a block
                    count += traverse(spring_cond, damaged_springs, a + 1, b + 1, 0)
            else:
                # move block length up
                count += traverse(spring_cond, damaged_springs, a + 1, b, length + 1)

    DP[dp_key] = count

    return count


def day12(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    result1 = 0
    result2 = 0
    for line in lines:
        line_split = line.split(" ")
        damaged_springs = [int(group) for group in line_split[1].split(",")]
        chars = list(line_split[0])

        result1 += traverse(chars, damaged_springs, 0, 0, 0)
        DP.clear()

        chars = list(
            "?".join(
                [
                    line_split[0],
                    line_split[0],
                    line_split[0],
                    line_split[0],
                    line_split[0],
                ]
            )
        )
        damaged_springs = [
            int(group)
            for group in ",".join(
                [
                    line_split[1],
                    line_split[1],
                    line_split[1],
                    line_split[1],
                    line_split[1],
                ]
            ).split(",")
        ]
        result2 += traverse(chars, damaged_springs, 0, 0, 0)
        DP.clear()

    print(f"result1: {result1}")
    print(f"result2: {result2}")


day12("sample.txt")
day12("input.txt")
