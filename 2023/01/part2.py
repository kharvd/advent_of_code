import sys


def find_all_spelled_out_digits(s):
    spelled_out_digits = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    all_digits = []
    for digit in spelled_out_digits:
        if digit in s:
            start_index = 0
            digit_int = spelled_out_digits.index(digit) + 1
            while True:
                index = s.find(digit, start_index)
                if index == -1:
                    break
                all_digits.append((index, digit_int))
                start_index = index + 1
    return sorted(all_digits)


def extract_digits(line):
    digits_with_index = [
        (index, int(digit)) for index, digit in enumerate(line) if digit.isdigit()
    ]
    spelled_out_digits_with_index = find_all_spelled_out_digits(line)
    print(digits_with_index)
    print(spelled_out_digits_with_index)
    all_digits_with_index = digits_with_index + spelled_out_digits_with_index
    return sorted(all_digits_with_index)


lines = sys.stdin.readlines()
sum = 0
for line in lines:
    digits_with_index = extract_digits(line)
    calibration_value = digits_with_index[0][1] * 10 + digits_with_index[-1][1]
    print(line, calibration_value)
    sum += calibration_value

print(sum)
