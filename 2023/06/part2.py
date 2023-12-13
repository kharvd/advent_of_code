import sys
import re


def distance_for_hold(race_duration, hold_duration):
    return hold_duration * max(0, race_duration - hold_duration)


def possible_distances(race_duration):
    distances = []
    for hold_duration in range(0, race_duration):
        distances.append(distance_for_hold(race_duration, hold_duration))
    return distances


def num_ways_to_beat(race_duration, current_record):
    options = possible_distances(race_duration)
    return len([x for x in options if x > current_record])


duration = int("".join([x for x in re.split(r"\s+", sys.stdin.readline())[1:-1]]))
record = int("".join([x for x in re.split(r"\s+", sys.stdin.readline())[1:-1]]))

print(num_ways_to_beat(duration, record))
