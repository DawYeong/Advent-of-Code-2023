import math


def day6(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")
    time_split = list(filter(lambda x: len(x) != 0, lines[0].split(" ")))[1:]
    distance_split = list(filter(lambda x: len(x) != 0, lines[1].split(" ")))[1:]

    times = [int(x) for x in time_split]
    distances = [int(x) for x in distance_split]

    time2 = int("".join(time_split))
    distance2 = int("".join(distance_split))

    result1 = 1

    for i in range(len(times)):
        sqrt = math.sqrt(math.pow(times[i], 2) - 4 * distances[i])
        lower_bound = (times[i] - sqrt) / 2
        upper_bound = (times[i] + sqrt) / 2
        lower_test = lower_bound % 1
        upper_test = upper_bound % 1

        shortest = math.ceil(lower_bound)
        longest = math.floor(upper_bound)

        if lower_test == 0:
            shortest += 1

        if upper_test == 0:
            longest -= 1

        result1 *= longest - shortest + 1

    print(f"result1: {result1}")

    sqrt2 = math.sqrt(math.pow(time2, 2) - 4 * distance2)
    lower_bound2 = (time2 - sqrt2) / 2
    upper_bound2 = (time2 + sqrt2) / 2
    lower_test2 = lower_bound2 % 1
    upper_test2 = upper_bound2 % 1

    shortest = math.ceil(lower_bound2)
    longest = math.floor(upper_bound2)

    if lower_test2 == 0:
        shortest += 1

    if upper_test2 == 0:
        longest -= 1

    result2 = longest - shortest + 1

    print(f"result2: {result2}")


day6("sample.txt")
day6("input.txt")
