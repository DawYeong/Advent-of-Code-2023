import copy


def day9(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")
    history = [[int(x) for x in line.split(" ")] for line in lines]

    result1 = 0
    result2 = 0
    for h in history:
        differences = []
        curr_diffs = copy.deepcopy(h)

        while len(list(filter(lambda x: x != 0, curr_diffs))) > 0:
            curr_diff = []
            for i in range(0, len(curr_diffs) - 1):
                temp_val = curr_diffs[i + 1] - curr_diffs[i]
                curr_diff.append(temp_val)
            differences.append(curr_diffs)
            curr_diffs = curr_diff

        acc1 = 0
        acc2 = 0
        for i in range(len(differences) - 1, -1, -1):
            acc1 += differences[i][len(differences[i]) - 1]
            acc2 = differences[i][0] - acc2

        result1 += acc1
        result2 += acc2

    print(f"result1: {result1}")
    print(f"result2: {result2}")


day9("sample.txt")
day9("input.txt")
