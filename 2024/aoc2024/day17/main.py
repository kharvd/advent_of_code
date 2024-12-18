from dataclasses import dataclass
import sys


@dataclass
class Computer:
    a: int
    b: int
    c: int
    pg: list[int]

    pc: int = 0

    def step(self):
        output = None
        if self.pc >= len(self.pg):
            return False, output

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
            output = self.combo(operand) % 8
        elif opcode == 6:
            self.b = self._adv(operand)
        elif opcode == 7:
            self.c = self._adv(operand)

        if not jumped:
            self.pc += 2

        return True, output

    def print_program(self):
        for i in range(0, len(self.pg), 2):
            opcode = self.pg[i]
            operand = self.pg[i + 1]
            print(i, end="\t")

            if opcode == 0:
                print(f"A = A // (1 << {self.combo_encode(operand)})")
            elif opcode == 1:
                print(f"B ^= {operand}")
            elif opcode == 2:
                print(f"B = {self.combo_encode(operand)} % 8")
            elif opcode == 3:
                print(f"if A != 0: goto {operand}")
            elif opcode == 4:
                print("B ^= C")
            elif opcode == 5:
                print(f"OUT {self.combo_encode(operand)} % 8")
            elif opcode == 6:
                print(f"B = A // (1 << {self.combo_encode(operand)})")
            elif opcode == 7:
                print(f"C = A // (1 << {self.combo_encode(operand)})")

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

    def combo_encode(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return "A"
        if operand == 5:
            return "B"
        if operand == 6:
            return "C"
        raise RuntimeError("invalid combo operand", operand)


def read_input():
    a = int(sys.stdin.readline().split(" ")[2])
    b = int(sys.stdin.readline().split(" ")[2])
    c = int(sys.stdin.readline().split(" ")[2])
    sys.stdin.readline()
    pg = [int(x) for x in sys.stdin.readline().split(" ")[1].split(",")]
    return Computer(a, b, c, pg)


def run_comp(comp):
    output = []
    while True:
        success, out = comp.step()
        if not success:
            break
        if out is not None:
            output.append(out)

    return ",".join(str(x) for x in output)


def part1():
    comp = read_input()
    print(run_comp(comp))


def get(arr, i):
    if i >= 0:
        return arr[i]
    return 0


def derive_next(pat: list[int], i, target):
    for j in range(8):
        if j == 0:
            c = (get(pat, i - 2) >> 1) ^ ((get(pat, i - 3) << 2) & 0b111)
        elif j == 1:
            c = get(pat, i - 2)
        elif j == 2:
            c = (get(pat, i - 1) >> 2) ^ ((get(pat, i - 2) << 1) & 0b111)
        elif j == 3:
            c = (get(pat, i - 1) >> 1) ^ ((get(pat, i - 2) << 2) & 0b111)
        elif j == 4:
            c = get(pat, i - 1)
        elif j == 5:
            c = (j >> 2) ^ ((get(pat, i - 1) << 1) & 0b111)
        elif j == 6:
            c = (j >> 1) ^ ((get(pat, i - 1) << 2) & 0b111)
        elif j == 7:
            c = j

        if c ^ j == target:
            yield j


def search(pat, pg, i):
    if i == len(pg):
        yield convert_pat(pat)
        return

    for c in derive_next(pat, i, pg[-(i + 1)]):
        pat[i] = c
        yield from search(pat, pg, i + 1)

    return


def convert_pat(pat):
    res = 0
    mult = 1
    for i in range(1, len(pat) + 1):
        res += pat[-i] * mult
        mult *= 8
    return res


def part2():
    comp = read_input()
    pg = comp.pg
    target = ",".join(str(x) for x in pg)
    print(pg)
    pat = [0] * (len(pg))

    for a in search(pat, pg, 0):
        test_comp = Computer(a, 0, 0, pg)
        if target == run_comp(test_comp):
            print(a)
            break


if __name__ == "__main__":
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
