import math

SEED_TO_SOIL = "seed-to-soil map:"
SOIL_TO_FERTILIZER = "soil-to-fertilizer map:"
FERTILIZER_TO_WATER = "fertilizer-to-water map:"
WATER_TO_LIGHT = "water-to-light map:"
LIGHT_TO_TEMPERATURE = "light-to-temperature map:"
TEMPERATURE_TO_HUMIDITY = "temperature-to-humidity map:"
HUMIDITY_TO_LOCATION = "humidity-to-location map:"

IDS = [
    SEED_TO_SOIL,
    SOIL_TO_FERTILIZER,
    FERTILIZER_TO_WATER,
    WATER_TO_LIGHT,
    LIGHT_TO_TEMPERATURE,
    TEMPERATURE_TO_HUMIDITY,
    HUMIDITY_TO_LOCATION,
]


def day5(filename):
    with open(filename, "r") as file:
        data = file.read()

    lines = list(filter(lambda x: len(x) != 0, data.split("\n")))

    seeds = [int(seed) for seed in lines[0].split(" ")[1:]]
    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append(range(seeds[i], seeds[i] + seeds[i + 1] + 1))

    id = ""
    mappings = {
        SEED_TO_SOIL: [],
        SOIL_TO_FERTILIZER: [],
        FERTILIZER_TO_WATER: [],
        WATER_TO_LIGHT: [],
        LIGHT_TO_TEMPERATURE: [],
        TEMPERATURE_TO_HUMIDITY: [],
        HUMIDITY_TO_LOCATION: [],
    }
    for el in lines[1:]:
        if el in IDS:
            id = el
        else:
            split = [int(x) for x in el.split(" ")]
            # elements are (source_begin, source_end, dest, rule)
            mappings[id].append((split[1], split[1] + split[2] - 1, split[0], split[2]))

    for id in IDS:
        mappings[id].sort(key=lambda x: x[0])

    def find_mapping(type, key):
        result = key
        for el in mappings[type]:
            if el[0] <= key <= el[1]:
                result = key - el[0] + el[2]
                break

        return result

    # 1: figuring out what fits into which rule
    # 2: figuring out what doesn't fit
    def calculate_range(type, ranges):
        result = []
        for rule in mappings[type]:
            rule_range = range(rule[0], rule[1] + 1)
            new_ranges = []
            for curr_range in ranges:
                intersection = [
                    max(curr_range.start, rule_range.start),
                    min(curr_range.stop, rule_range.stop),
                ]

                if intersection[0] >= intersection[1]:
                    new_ranges.append(curr_range)
                    continue

                lower_diff = intersection[0] - curr_range.start
                upper_diff = curr_range.stop - intersection[1]

                result.append(
                    range(
                        intersection[0] - rule[0] + rule[2],
                        intersection[1] - rule[0] + rule[2],
                    )
                )

                if lower_diff > 0:
                    new_ranges.append(range(curr_range.start, intersection[0]))

                if upper_diff > 0:
                    new_ranges.append(range(intersection[1], curr_range.stop))

            ranges = new_ranges

        result.extend(ranges)
        return result

    min_loc = math.inf

    for seed in seeds:
        soil_loc = find_mapping(SEED_TO_SOIL, seed)
        fertilizer_loc = find_mapping(SOIL_TO_FERTILIZER, soil_loc)
        water_loc = find_mapping(FERTILIZER_TO_WATER, fertilizer_loc)
        light_loc = find_mapping(WATER_TO_LIGHT, water_loc)
        temperature_loc = find_mapping(LIGHT_TO_TEMPERATURE, light_loc)
        humidity_loc = find_mapping(TEMPERATURE_TO_HUMIDITY, temperature_loc)
        location = find_mapping(HUMIDITY_TO_LOCATION, humidity_loc)

        min_loc = min(min_loc, location)

    print(f"result1: {min_loc}")

    soil_locs = calculate_range(SEED_TO_SOIL, ranges)
    fertilizer_locs = calculate_range(SOIL_TO_FERTILIZER, soil_locs)
    water_locs = calculate_range(FERTILIZER_TO_WATER, fertilizer_locs)
    light_locs = calculate_range(WATER_TO_LIGHT, water_locs)
    temperature_locs = calculate_range(LIGHT_TO_TEMPERATURE, light_locs)
    humidity_locs = calculate_range(TEMPERATURE_TO_HUMIDITY, temperature_locs)
    locations = calculate_range(HUMIDITY_TO_LOCATION, humidity_locs)

    min_loc2 = min([r.start for r in locations])
    print(f"result2: {min_loc2}")


day5("sample.txt")
day5("input.txt")
