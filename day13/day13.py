def day13(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    patterns = []
    curr = []
    for line in lines:
        if len(line) == 0:
            patterns.append(curr)
            curr = []
        else:
            curr.append(line)

    patterns.append(curr)

    def check_horizontal(pattern, left, right, smudge):
        if left < 0 or right >= len(pattern):
            return True, smudge

        diff = len(
            [
                i
                for i in range(len(pattern[left]))
                if pattern[left][i] != pattern[right][i]
            ]
        )
        if diff == 0:
            return check_horizontal(pattern, left - 1, right + 1, smudge)
        elif diff == 1:
            if smudge:
                return False, smudge
            else:
                return check_horizontal(pattern, left - 1, right + 1, 1)
        else:
            return False, smudge

    def check_vertical(pattern, up, down, smudge):
        if up < 0 or down >= len(pattern[0]):
            return True, smudge

        up_line = [x[up] for x in pattern]
        down_line = [x[down] for x in pattern]

        diff = len([i for i in range(len(up_line)) if up_line[i] != down_line[i]])
        if diff == 0:
            return check_vertical(pattern, up - 1, down + 1, smudge)
        elif diff == 1:
            if smudge:
                return False, smudge
            else:
                return check_vertical(pattern, up - 1, down + 1, 1)
        else:
            return False, smudge

    for p in [0, 1]:
        result = 0
        for pattern in patterns:
            vertical = -1
            for i in range(len(pattern[0]) - 1):
                valid, smudge = check_vertical(pattern, i, i + 1, 0)
                if (not p and valid and not smudge) or (p and valid and smudge):
                    vertical = i
                    break

            if vertical > -1:
                result += vertical + 1

            horizontal = -1
            for i in range(len(pattern) - 1):
                valid, smudge = check_horizontal(pattern, i, i + 1, 0)
                if (not p and valid and not smudge) or (p and valid and smudge):
                    horizontal = i
                    break

            if horizontal > -1:
                result += (horizontal + 1) * 100

        if not p:
            print(f"result1: {result}")
        else:
            print(f"result2: {result}")


day13("sample.txt")
day13("input.txt")
