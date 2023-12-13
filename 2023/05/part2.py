import sys


def get_seeds():
    return list(map(int, sys.stdin.readline().split(": ")[1].split(" ")))


def get_ranges():
    ranges = []
    while line := sys.stdin.readline().strip():
        to, fro, l = map(int, line.split(" "))
        ranges.append((to, fro, l))
    return ranges


def get_map():
    sys.stdin.readline()
    ranges = get_ranges()

    ranges = [((fro, fro + l), (to, to + l)) for to, fro, l in ranges]

    ranges.sort(key=lambda x: x[0][0])

    all_ranges = []

    if ranges[0][0][0] != 0:
        all_ranges.append(((0, ranges[0][0][0]), (0, ranges[0][0][0])))

    for i in range(len(ranges)):
        if ranges[i][0][0] != ranges[i - 1][0][1]:
            all_ranges.append(
                (
                    (ranges[i - 1][0][1], ranges[i][0][0]),
                    (ranges[i - 1][0][1], ranges[i][0][0]),
                )
            )
        all_ranges.append(ranges[i])

    all_ranges.append(
        ((ranges[-1][0][1], 1000000000000), (ranges[-1][0][1], 1000000000000))
    )

    ranges = all_ranges

    def get_dest(seed_range):
        seed_start = seed_range[0]
        for range_i, ((fro_start, fro_end), (to_start, to_end)) in enumerate(ranges):
            if fro_start <= seed_start < fro_end:
                dest_start = to_start + (seed_start - fro_start)
                range_start = range_i
                break
        else:
            raise ValueError("Invalid seed range")

        seed_end = seed_range[1]
        for range_i, ((fro_start, fro_end), (to_start, to_end)) in enumerate(
            ranges[::-1]
        ):
            if fro_start < seed_end <= fro_end:
                dest_end = to_start + (seed_end - fro_start)
                range_end = len(ranges) - range_i - 1
                break
        else:
            raise ValueError("Invalid seed range")

        new_ranges = [
            (to_start, to_end)
            for _, (to_start, to_end) in ranges[range_start : range_end + 1]
        ]
        new_ranges[0] = (dest_start, new_ranges[0][1])
        new_ranges[-1] = (new_ranges[-1][0], dest_end)

        return new_ranges

    return get_dest


seeds = get_seeds()
sys.stdin.readline()
seed_to_soil = get_map()
soil_to_fertilizer = get_map()
fertilizer_to_water = get_map()
water_to_light = get_map()
light_to_temperature = get_map()
temperature_to_humidity = get_map()
humidity_to_location = get_map()

locations = []
for i in range(0, len(seeds), 2):
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1])]
    soil_ranges = [
        ran for seed_range in seed_ranges for ran in seed_to_soil(seed_range)
    ]
    fertilizer_ranges = [
        ran for soil_range in soil_ranges for ran in soil_to_fertilizer(soil_range)
    ]
    water_ranges = [
        ran
        for fertilizer_range in fertilizer_ranges
        for ran in fertilizer_to_water(fertilizer_range)
    ]
    light_ranges = [
        ran for water_range in water_ranges for ran in water_to_light(water_range)
    ]
    temperature_ranges = [
        ran for light_range in light_ranges for ran in light_to_temperature(light_range)
    ]
    humidity_ranges = [
        ran
        for temperature_range in temperature_ranges
        for ran in temperature_to_humidity(temperature_range)
    ]
    location_ranges = [
        ran
        for humidity_range in humidity_ranges
        for ran in humidity_to_location(humidity_range)
    ]
    locations.extend(location_ranges)

locations.sort()
print(locations[0][0])
