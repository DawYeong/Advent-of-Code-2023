from collections import defaultdict


def simulate(bricks):
    highest_block = defaultdict(lambda: (0, None))
    cannot_remove = set()
    graph = defaultdict(set)
    dependency_count = defaultdict(int)

    for idx, brick in enumerate(bricks):
        lowest_height = 0
        # keep track of what dependencies each brick has
        dependencies = set()

        # figure out lowest height the brick can fall to
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                if highest_block[x, y][0] >= lowest_height:
                    lowest_height = highest_block[x, y][0] + 1
                    dependencies = {highest_block[x, y][1]}
                elif highest_block[x, y][0] + 1 == lowest_height:
                    dependencies.add(highest_block[x, y][1])

        fall_dist = brick[0][2] - lowest_height if brick[0][2] > lowest_height else 0
        brick[0][2] -= fall_dist
        brick[1][2] -= fall_dist

        for item in dependencies:
            graph[item].add(idx)

        dependency_count[idx] = len(dependencies)
        # nodes that cannot be removed can be found from bricks that only have a single dependency
        if len(dependencies) == 1:
            item = next(iter(dependencies))
            if item != None:
                cannot_remove.add(item)

        # update highest_block
        for x in range(brick[0][0], brick[1][0] + 1):
            for y in range(brick[0][1], brick[1][1] + 1):
                highest_block[x, y] = (brick[1][2], idx)

    return len(bricks) - len(cannot_remove), graph, dependency_count


def fall_count(n, graph, dependency_count):
    total = 0
    for i in range(n):
        state = defaultdict(int)
        work_list = [i]
        count = -1
        while work_list:
            count += 1
            item = work_list.pop(0)

            for el in graph[item]:
                state[el] += 1
                if state[el] == dependency_count[el]:
                    # item falls
                    work_list.append(el)
        total += count

    return total


def day22(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    bricks = []
    for line in lines:
        coords = [
            [int(x) for x in line_split.split(",")] for line_split in line.split("~")
        ]
        bricks.append(coords)

    bricks.sort(key=lambda x: x[0][2])

    result1, graph, dependency_count = simulate(bricks)
    print(f"result1: {result1}")

    result2 = fall_count(len(bricks), graph, dependency_count)
    print(f"result2: {result2}")


day22("sample.txt")
day22("input.txt")
