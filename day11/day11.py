def day11(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = data.split("\n")

    empty_rows = []
    for i in range(len(lines)):
        if len(list(filter(lambda x: x == "#", lines[i]))) == 0:
            empty_rows.append(i)

    empty_cols = []
    for i in range(len(lines[0])):
        if len(list(filter(lambda x: x == "#", [line[i] for line in lines]))) == 0:
            empty_cols.append(i)

    galaxies = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "#":
                galaxies.append((i, j))

    def find_shortest_distances(expansion_factor):
        result = 0
        for i in range(len(galaxies) - 1):
            for j in range(i + 1, len(galaxies)):
                row_gaps = len(
                    list(
                        filter(
                            lambda x: galaxies[i][0] < x < galaxies[j][0], empty_rows
                        )
                    )
                )
                col_lower = min(galaxies[i][1], galaxies[j][1])
                col_upper = max(galaxies[i][1], galaxies[j][1])
                col_gaps = len(
                    list(filter(lambda x: col_lower < x < col_upper, empty_cols))
                )
                result += (
                    abs(galaxies[i][0] - galaxies[j][0])
                    + abs(galaxies[i][1] - galaxies[j][1])
                    + (expansion_factor - 1) * (row_gaps + col_gaps)
                )

        return result

    result1 = find_shortest_distances(2)
    result2 = find_shortest_distances(1000000)

    print(f"result1: {result1}")
    print(f"result2: {result2}")


day11("sample.txt")
day11("input.txt")
