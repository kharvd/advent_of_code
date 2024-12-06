import sys


def check_update(rules, update):
    for rule in rules:
        try:
            index1 = update.index(rule[0])
            index2 = update.index(rule[1])
            if index1 > index2:
                return False
        except ValueError:
            continue
    return True


def read_input():
    rules = []
    while (line := sys.stdin.readline().strip()) != "":
        rules.append(tuple(map(lambda x: int(x), line.split("|"))))

    updates = []
    while line := sys.stdin.readline().strip():
        updates.append(list(map(lambda x: int(x), line.split(","))))
    return set(rules), updates


def sort_update(rules, update):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if (update[j], update[i]) in rules:
                update[i], update[j] = update[j], update[i]
            elif (update[i], update[j]) in rules:
                continue
            else:
                raise ValueError("Not a total order")
    return update


def part1():
    rules, updates = read_input()
    s = 0
    for update in updates:
        if check_update(rules, update):
            s += update[len(update) // 2]
    return s


def part2():
    rules, updates = read_input()
    s = 0
    for update in updates:
        if not check_update(rules, update):
            sort_update(rules, update)
            s += update[len(update) // 2]
    return s


if __name__ == "__main__":
    if sys.argv[1] == "1":
        print(part1())
    elif sys.argv[1] == "2":
        print(part2())
