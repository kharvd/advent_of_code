from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass
import math
import sys
from typing import List

import tqdm


@dataclass
class Signal:
    fro: str
    to: str
    level: bool


class Module(ABC):
    def __init__(self, name: str):
        self.inputs = []
        self.outputs = []
        self.name = name

    def add_input(self, input: str):
        self.inputs.append(input)

    def add_output(self, output: str):
        self.outputs.append(output)

    @abstractmethod
    def process(self, input: str, level: bool) -> List[Signal]:
        pass


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.on = False

    def process(self, input: str, level: bool) -> List[Signal]:
        if not level:
            self.on = not self.on
            return [Signal(self.name, n, self.on) for n in self.outputs]
        return []


class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {}

    def add_input(self, input: str):
        super().add_input(input)
        self.memory[input] = False

    def process(self, input: str, level: bool) -> List[Signal]:
        self.memory[input] = level
        all_true = True
        for input in self.memory:
            all_true = all_true and self.memory[input]

        return [Signal(self.name, n, not all_true) for n in self.outputs]


class Broadcaster(Module):
    def __init__(self, name):
        super().__init__(name)

    def process(self, input: str, level: bool) -> List[Signal]:
        return [Signal(self.name, n, level) for n in self.outputs]


class System:
    def __init__(self, modules: dict[str, Module]):
        self.modules = modules
        self.signal_count = {
            False: 0,
            True: 0,
        }
        self.num_button_presses = 0
        self.first_low_signal = {}

    def press_button(self):
        self.num_button_presses += 1
        queue = deque([Signal("button", "broadcaster", False)])

        while len(queue) > 0:
            signal = queue.popleft()

            self.signal_count[signal.level] += 1
            # print(f"{signal.fro} -{'high' if signal.level else 'low'}-> {signal.to}")
            if signal.to in ["bp", "xc", "th", "pd"] and not signal.level:
                print(f"low signal received at {signal.to}")
                print(f"num button presses: {self.num_button_presses}")
                self.first_low_signal[signal.to] = self.num_button_presses

            module = self.modules.get(signal.to)
            if module:
                for output in module.process(signal.fro, signal.level):
                    queue.append(output)

    @staticmethod
    def read() -> "System":
        modules = {}
        module_inputs: dict[str, list[str]] = defaultdict(list)
        for line in sys.stdin:
            fro, to = line.strip().split(" -> ")
            if fro == "broadcaster":
                module = Broadcaster(fro)
            elif fro.startswith("%"):
                module = FlipFlop(fro[1:])
            elif fro.startswith("&"):
                module = Conjunction(fro[1:])
            else:
                assert False

            for output in to.split(", "):
                module.add_output(output)
                module_inputs[output].append(module.name)
            modules[module.name] = module

        for module in modules.values():
            for input in module_inputs[module.name]:
                module.add_input(input)

        return System(modules)

    def print_graphviz(self):
        def module_name(name):
            if name in self.modules:
                return f"{type(self.modules[name]).__name__}_{name}"
            return name

        print("digraph G {")
        for module in self.modules.values():
            for output in module.outputs:
                print(f"{module_name(module.name)} -> {module_name(output)};")
        print("}")


def lcm(*args):
    return math.prod(args) // math.gcd(*args)


system = System.read()

for _ in range(100000000):
    system.press_button()
    if len(system.first_low_signal) == 4:
        break

print(lcm(*system.first_low_signal.values()))
