from dataclasses import dataclass
import sys


@dataclass
class Computer:
    a: int
    b: int
    c: int
    pg: list[int]

    pc: int = 0

    out = []

    def step(self):
        if self.pc >= len(self.pg):
            return False

        opcode = self.pg[self.pc]
        operand = self.pg[self.pc + 1]
        jumped = False
        if opcode == 0:
            self.a = self._adv(operand)
        elif opcode == 1:
            self.b ^= operand
        elif opcode == 2:
            self.b = self.combo(operand) % 8
        elif opcode == 3:
            if self.a != 0:
                self.pc = operand
                jumped = True
        elif opcode == 4:
            self.b ^= self.c
        elif opcode == 5:
            self.output(self.combo(operand) % 8)
        elif opcode == 6:
            self.b = self._adv(operand)
        elif opcode == 7:
            self.c = self._adv(operand)

        if not jumped:
            self.pc += 2

        return True

    def _adv(self, operand):
        numerator = self.a
        denominator = 2 ** self.combo(operand)
        return numerator // denominator

    def combo(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise RuntimeError("invalid combo operand")

    def output(self, x):
        self.out.append(x)


def read_input():
    a = int(sys.stdin.readline().split(" ")[2])
    b = int(sys.stdin.readline().split(" ")[2])
    c = int(sys.stdin.readline().split(" ")[2])
    sys.stdin.readline()
    pg = [int(x) for x in sys.stdin.readline().split(" ")[1].split(",")]
    return Computer(a, b, c, pg)


def part1():
    comp = read_input()
    while comp.step():
        pass

    print(",".join(str(x) for x in comp.out))


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
