from collections import defaultdict
import copy

CONDITIONS_KEY = "CONDITIONS"
END_KEY = "END"


def day19(filename):
    with open(filename, "r") as file:
        data = file.read()

    sections = data.split("\n\n")

    conditions = defaultdict(dict)
    for s in sections[0].split("\n"):
        open_ind = s.index("{")
        id = s[0:open_ind]
        cond = s[open_ind + 1 : len(s) - 1].split(",")
        conditions[id][CONDITIONS_KEY] = []
        for i in range(len(cond) - 1):
            dest = cond[i].index(":")
            conditions[id][CONDITIONS_KEY].append(
                (
                    cond[i][0],
                    cond[i][1],
                    int(cond[i][2:dest]),
                    cond[i][dest + 1 :],
                )
            )

        conditions[id][END_KEY] = cond[len(cond) - 1]

    accepted = []
    for part in sections[1].split("\n"):
        components = {}
        for component in part[1 : len(part) - 1].split(","):
            components[component[0]] = int(component[2:])

        pos = "in"
        while pos != "R" and pos != "A":
            c = conditions[pos]
            pos = c[END_KEY]

            for cond in c[CONDITIONS_KEY]:
                check = (
                    components[cond[0]] > cond[2]
                    if cond[1] == ">"
                    else components[cond[0]] < cond[2]
                )
                if check:
                    pos = cond[3]
                    break

        if pos == "A":
            accepted.append(components)

    result1 = 0
    for components in accepted:
        result1 += sum(list(components.values()))

    print(f"result1: {result1}")

    pos = "in"
    parts = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}

    def traverse(id, parts_state):
        if id == "R":
            return 0
        elif id == "A":
            combo = 1
            for v in parts_state.values():
                combo *= v[1] - v[0] + 1
            return combo
        c = conditions[id]
        res = 0
        for cond in c[CONDITIONS_KEY]:
            # find the ranges for each condition
            new_state_value = (
                max(parts_state[cond[0]][0], cond[2] + 1)
                if cond[1] == ">"
                else parts_state[cond[0]][0],
                min(parts_state[cond[0]][1], cond[2] - 1)
                if cond[1] == "<"
                else parts_state[cond[0]][1],
            )

            if new_state_value[0] > new_state_value[1]:
                continue
            parts_state_copy = copy.deepcopy(parts_state)
            parts_state_copy[cond[0]] = new_state_value
            res += traverse(cond[3], parts_state_copy)

            # update range for next condition (the opposite range calculated from above)
            parts_state[cond[0]] = (
                new_state_value[1] + 1 if cond[1] == "<" else parts_state[cond[0]][0],
                new_state_value[0] - 1 if cond[1] == ">" else parts_state[cond[0]][1],
            )

        res += traverse(c[END_KEY], parts_state)

        return res

    result2 = traverse(pos, parts)
    print(f"result2: {result2}")


day19("sample.txt")
day19("input.txt")
