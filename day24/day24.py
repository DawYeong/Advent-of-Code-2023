from fractions import Fraction
import numpy as np
import math


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

    # PART 2
    # find any three hailstones that are independent
    def find_independent_hailstones():
        for i in range(len(hailstones) - 2):
            for j in range(i + 1, len(hailstones) - 1):
                for k in range(j + 1, len(hailstones)):
                    test1 = np.cross(hailstones[i][1], hailstones[j][1])
                    test2 = np.cross(hailstones[i][1], hailstones[k][1])
                    test3 = np.cross(hailstones[j][1], hailstones[k][1])

                    if not (
                        all(v == 0 for v in test1)
                        or all(v == 0 for v in test2)
                        or all(v == 0 for v in test3)
                    ):
                        return [hailstones[i], hailstones[j], hailstones[k]]

        return None

    part2_hailstones = find_independent_hailstones()
    assert len(part2_hailstones) == 3

    # 1) for a rock to hit some hailstone at time t: r + vr*t = h1 + vh1*t => r = h1 + (vh1 - vr)*t

    # given two hailstones, the plane created (assuming hailstones are independent) is (h1 - h2) . (vh1 x vh2) = P1
    # to determine if two rays will intersect we can make sure that the vectors are independent and they are coplanar
    # from 1) the formula forms a new vector starting at hi with vector (vhi - vr)
    # now to find out if the point of intersections of rock form a plane: (h1 - h2) . (vh1 - vr) x (vh2 - vr) = 0
    # some simplifications => vr . (vh1 - vh2) * (h1 - h2) = P1
    # since we have 3 variables => we need 3 equations
    p2_equations = []

    # determine the planes
    for i in range(len(part2_hailstones)):
        point_diff = np.subtract(
            part2_hailstones[i][0],
            part2_hailstones[(i + 1) % len(part2_hailstones)][0],
        )
        p = np.dot(
            point_diff,
            np.cross(
                part2_hailstones[i][1],
                part2_hailstones[(i + 1) % len(part2_hailstones)][1],
            ),
        )
        coeffs = np.cross(
            point_diff,
            np.subtract(
                part2_hailstones[i][1],
                part2_hailstones[(i + 1) % len(part2_hailstones)][1],
            ),
        )
        p = Fraction(p, coeffs[0])
        coeffs = [Fraction(c, coeffs[0]) for c in coeffs]

        p2_equations.append((coeffs, p))

    # # row reduction to find velocity
    for row in range(len(p2_equations) - 1):
        for reduce in range(row + 1, len(p2_equations)):
            coeffs_red = np.subtract(p2_equations[row][0], p2_equations[reduce][0])
            p_red = p2_equations[row][1] - p2_equations[reduce][1]

            p_red = p_red / coeffs_red[row + 1]
            temp = coeffs_red[row + 1]
            for s in range(row + 1, len(p2_equations)):
                coeffs_red[s] /= temp

            p2_equations[reduce] = (coeffs_red, p_red)

    velocity = [p2_equations[2][1]]
    velocity.insert(0, p2_equations[1][1] - velocity[0] * p2_equations[1][0][2])
    velocity.insert(
        0,
        p2_equations[0][1]
        - velocity[1] * p2_equations[0][0][2]
        - velocity[0] * p2_equations[0][0][1],
    )

    # simplify fractions
    lcm = 1
    for vel in velocity:
        lcm = lcm * vel.denominator // math.gcd(lcm, vel.denominator)

    velocity = [vel * lcm for vel in velocity]

    print(f"velocity: {velocity}")

    # now that we have the velocity, we can find the initial point using 2 of the hailstones
    # from the viewpoint of the rock, we can solve h1 + (v1 - vr) * t = h2 + (v2 - vr) * s
    # we will have 3 equations with 2 unknowns (s,t) => trim it down to 2 unknowns

    hail_vel1 = [int(x) for x in np.subtract(part2_hailstones[0][1], velocity)]
    hail_vel2 = [int(x) for x in np.subtract(part2_hailstones[1][1], velocity)]
    coeffs = [[hail_vel1[i], -hail_vel2[i]] for i in range(2)]
    hail_pos = np.subtract(part2_hailstones[1][0], part2_hailstones[0][0])[:2]

    s_t_results = np.linalg.solve(coeffs, hail_pos)

    # only need to calculate the position using one of the result
    result2 = int(
        sum(
            [
                (part2_hailstones[0][0][i] + hail_vel1[i] * s_t_results[0])
                for i in range(3)
            ]
        )
    )
    print(f"result2: {result2}")


day24("sample.txt", 7, 27)
day24("input.txt", 200000000000000, 400000000000000)
