import re


def day1_part1(filename):
    with open(filename, "r") as file:
        data = file.read().split("\n")

    sum = 0
    for line in data:
        numbers = [c for c in line if c.isnumeric()]
        sum += int("".join([numbers[0], numbers[-1]]))

    return sum


def day1_part2(filename):
    with open(filename, "r") as file:
        data = file.read()

    # issue is that when we have something like twoneight => regex will only get two instead of [two, one, eight]
    # if we replace each word number with number#number => we can solve this issue
    data = (
        data.replace("one", "one1one")
        .replace("two", "two2two")
        .replace("three", "three3three")
        .replace("four", "four4four")
        .replace("five", "five5five")
        .replace("six", "six6six")
        .replace("seven", "seven7seven")
        .replace("eight", "eight8eight")
        .replace("nine", "nine9nine")
        .split("\n")
    )
    sum = 0
    for line in data:
        find = re.findall(r"\d", line)
        sum += int("".join([find[0], find[-1]]))

    return sum


sample = day1_part1("sample_part1.txt")
print(sample)

test = day1_part1("input.txt")
print(test)

sample_2 = day1_part2("sample_part2.txt")
print(sample_2)

test_2 = day1_part2("test2.txt")
print(test_2)

test_2 = day1_part2("input.txt")
print(test_2)
