from fractions import Fraction


def day24(filename, lower, upper):
    with open(filename, "r") as file:
        data = file.read().replace(" ", "")

    hailstones = [
        [[int(c) for c in section.split(",")] for section in line.split("@")]
        for line in data.split("\n")
    ]

    # y = mx + b
    equations = []

    for hailstone in hailstones:
        slope = Fraction(hailstone[1][1], hailstone[1][0])
        y_intercept = hailstone[0][1] - slope * hailstone[0][0]

        # want in the form of x + ay = b
        # we have -mx + y = b
        # transform it to: x - y/m = -b/m

        a = -1 / slope
        b = -y_intercept / slope

        equations.append((a, b))

    result1 = 0
    for i in range(len(equations) - 1):
        for j in range(i + 1, len(equations)):
            # two scenarios: no intercepts or infinite # of intercepts (same line) => for this problem assuming if this doesn't happen
            if equations[i][0] == equations[j][0]:
                continue

            # row reduction
            a_diff = equations[i][0] - equations[j][0]
            b_diff = equations[i][1] - equations[j][1]

            y = b_diff / a_diff

            if y < lower or y > upper:
                continue

            x = equations[i][1] - y * equations[i][0]

            if x < lower or x > upper:
                continue

            # have to check if paths crossed in the past or future

            if (
                (hailstones[i][0][0] > x and hailstones[i][1][0] > 0)
                or (hailstones[i][0][0] < x and hailstones[i][1][0] < 0)
                or (hailstones[j][0][0] > x and hailstones[j][1][0] > 0)
                or (hailstones[j][0][0] < x and hailstones[j][1][0] < 0)
            ):
                continue

            result1 += 1

    print(f"result1: {result1}")


day24("sample.txt", 7, 27)
day24("input.txt", 200000000000000, 400000000000000)
