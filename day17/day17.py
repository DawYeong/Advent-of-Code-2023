from heapq import heappush, heappop

DIRECTION = {
    0: (0, 1),  # right
    1: (1, 0),  # down
    2: (0, -1),  # left
    3: (-1, 0),  # up
}


def dijkstra(grid, start, end, min_steps, max_steps):
    priority_queue = [(0, *start)]
    seen = set()

    while priority_queue:
        cost, i, j, dir = heappop(priority_queue)
        if (i, j) == end:
            return cost

        if (i, j, dir) in seen:
            continue

        seen.add((i, j, dir))

        for key, value in DIRECTION.items():
            if dir != -1 and ((dir + 2) % 4 == key or dir == key):
                continue

            curr_i = i
            curr_j = j
            curr_cost = cost

            for step in range(1, max_steps + 1):
                curr_i += value[0]
                curr_j += value[1]
                if (curr_i, curr_j) not in grid:
                    continue

                curr_cost += grid[curr_i, curr_j]
                if step >= min_steps:
                    heappush(priority_queue, (curr_cost, curr_i, curr_j, key))


def day17(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = {
        (i, j): int(c)
        for i, line in enumerate(data.split("\n"))
        for j, c in enumerate(line)
    }

    result1 = dijkstra(lines, (0, 0, -1), max(lines), 1, 3)

    print(f"result1: {result1}")

    result2 = dijkstra(lines, (0, 0, -1), max(lines), 4, 10)

    print(f"result2: {result2}")


day17("sample.txt")
day17("input.txt")
