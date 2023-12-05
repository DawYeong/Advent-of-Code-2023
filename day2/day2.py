PART1_RESTRICTIONS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def day2_part1(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.replace(":", "").replace(";", "").replace(",", "").split("\n")
    result = 0
    for line in lines:
        # parse line
        split = line.split(" ")[1:]
        id = int(split[0])
        max_set = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for i in range(1, len(split), 2):
            max_set[split[i + 1]] = max(max_set[split[i + 1]], int(split[i]))

        if (
            max_set["blue"] <= PART1_RESTRICTIONS["blue"]
            and max_set["green"] <= PART1_RESTRICTIONS["green"]
            and max_set["red"] <= PART1_RESTRICTIONS["red"]
        ):
            result += id

    return result


def day2_part2(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.replace(":", "").replace(";", "").replace(",", "").split("\n")
    result = 0
    for line in lines:
        # pretty much part 1 but multiply the max
        split = line.split(" ")[2:]
        max_set = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for i in range(0, len(split), 2):
            max_set[split[i + 1]] = max(max_set[split[i + 1]], int(split[i]))

        result += max_set["blue"] * max_set["green"] * max_set["red"]

    return result


sample1 = day2_part1("sample.txt")
print(sample1)

input1 = day2_part1("input.txt")
print(input1)

sample2 = day2_part2("sample.txt")
print(sample2)

input2 = day2_part2("input.txt")
print(input2)
