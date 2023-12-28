import sys
from collections import defaultdict

sys.setrecursionlimit(1000000)

EXCLUDE = {
    ".": set(),
    ">": set([(0, -1), (1, 0), (-1, 0)]),
    "<": set([(0, 1), (1, 0), (-1, 0)]),
    "^": set([(0, 1), (0, -1), (-1, 0)]),
    "v": set([(0, 1), (0, -1), (-1, 0)]),
}


def day23(filename):
    with open(filename, "r") as file:
        data = file.read()

    grid = {
        (i, j): c for i, line in enumerate(data.split("\n")) for j, c in enumerate(line)
    }
    start = (0, 1)
    end_corner = max(grid)
    end = (end_corner[0], end_corner[1] - 1)

    def dfs(start, end, part1=True, junctions=None):
        seen = set()
        costs = {start: 0}

        def explore(pos, curr_cost):
            costs[pos] = max(costs.get(pos, 0), curr_cost)

            seen.add(pos)
            items = (
                {
                    (pos[0] + dy, pos[1] + dx): 1
                    for dy, dx in {(0, 1), (0, -1), (1, 0), (-1, 0)}
                    - (EXCLUDE[grid[pos]])
                }.items()
                if part1
                else junctions[pos].items()
            )

            for k, v in items:
                if k not in grid or k in seen or grid[k] == "#":
                    continue

                explore(k, curr_cost + v)

            seen.remove(pos)

        explore(start, 0)

        return costs[end]

    result1 = dfs(start, end)

    print(f"result1: {result1}")

    def find_junctions(s, e):
        junctions = defaultdict(dict)
        junction_keys = set()
        work_list = [[0, s, s]]
        seen = set()

        while work_list:
            cost, pos, junction = work_list.pop()

            seen.add(pos)

            if pos == e:
                junctions[e][junction] = cost
                junctions[junction][e] = cost
                continue

            new_items = []
            new_cost = cost + 1
            for dy, dx in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
                new_pos = (pos[0] + dy, pos[1] + dx)

                if new_pos in junction_keys and junction != new_pos:
                    # if a junction to already found junction
                    junctions[junction][new_pos] = new_cost + 1
                    junctions[new_pos][junction] = new_cost + 1
                    continue

                if new_pos not in grid or new_pos in seen or grid[new_pos] == "#":
                    continue

                new_items.append([new_cost, new_pos, junction])

            if len(new_items) >= 2:
                # found a new junction
                junctions[junction][pos] = new_cost
                junctions[pos][junction] = new_cost
                junction_keys.add(pos)
                for i in range(len(new_items)):
                    # reset cost
                    new_items[i][0] = 0
                    # update junction
                    new_items[i][2] = pos

            work_list.extend(new_items)

        return junctions

    junctions = find_junctions(start, end)

    result2 = dfs(start, end, False, junctions)

    print(f"result2: {result2}")


day23("sample.txt")
day23("input.txt")
