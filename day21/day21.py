from collections import deque


# lagrange formula for quadratic formula given x
def quad_lagrange(points, x):
    f0 = (points[0][1] * (x - points[1][0]) * (x - points[2][0])) / (
        (points[0][0] - points[1][0]) * (points[0][0] - points[2][0])
    )

    f1 = (points[1][1] * (x - points[0][0]) * (x - points[2][0])) / (
        (points[1][0] - points[0][0]) * (points[1][0] - points[2][0])
    )

    f2 = (points[2][1] * (x - points[0][0]) * (x - points[1][0])) / (
        (points[2][0] - points[0][0]) * (points[2][0] - points[1][0])
    )

    return int(f0 + f1 + f2)


def day21(filename, num_step):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    def find_start():
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "S":
                    return (i, j)

    start = find_start()

    def bfs(start, points_of_interest):
        todo = deque()
        todo.append(start)
        # to avoid revisiting the same node repeatedly
        visited = {start: 0}
        step = 0

        points = []

        while step < max(points_of_interest):
            step += 1
            new_todo = deque()

            while todo:
                y, x = todo.popleft()
                for dy, dx in {(0, 1), (1, 0), (0, -1), (-1, 0)}:
                    next_item = (y + dy, x + dx)
                    if (
                        lines[next_item[0] % len(lines)][next_item[1] % len(lines[0])]
                        != "#"
                        and next_item not in visited
                    ):
                        visited[next_item] = step
                        new_todo.append(next_item)

            todo = new_todo

            if step in points_of_interest:
                # only odd steps can reach positions from previous odd steps (even with evens)
                points.append(
                    (step, len([s for s in visited.values() if s % 2 == step % 2]))
                )

        return points

    result1 = bfs(start, [num_step])[0][1]

    print(f"result1: {result1}")

    size = len(lines)
    points = bfs(start, {size // 2, size // 2 + size, size // 2 + 2 * size})
    # print(test)
    result2 = quad_lagrange(points, 26501365)

    # not too sure if this works with the sample, solution is pretty specific to input
    print(f"result2: {result2}")


# day21("sample.txt", 6)
day21("input.txt", 64)
