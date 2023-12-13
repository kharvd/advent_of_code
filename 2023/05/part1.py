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

    def get_dest(seed):
        for to, fro, l in ranges:
            if fro <= seed <= fro + l:
                return to + (seed - fro)
        return seed

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
for seed in seeds:
    soil = seed_to_soil(seed)
    fertilizer = soil_to_fertilizer(soil)
    water = fertilizer_to_water(fertilizer)
    light = water_to_light(water)
    temperature = light_to_temperature(light)
    humidity = temperature_to_humidity(temperature)
    location = humidity_to_location(humidity)
    locations.append(location)

print(min(locations))
