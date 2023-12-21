from abc import ABC, abstractmethod
import sys
from typing import List, Optional, TypedDict, cast


class Part(TypedDict):
    x: int
    m: int
    a: int
    s: int


def parse_part(s: str) -> Part:
    s = s[1:-1]
    var_assignments = s.split(",")
    part = {}
    for var_assignment in var_assignments:
        var, value = var_assignment.split("=")
        part[var.strip()] = int(value.strip())
    return cast(Part, part)


def read_parts() -> List[Part]:
    parts = []
    for line in sys.stdin:
        parts.append(parse_part(line.strip()))
    return parts


class Rule(ABC):
    @abstractmethod
    def test(self, part: Part) -> Optional[str]:
        pass

    @staticmethod
    def parse(s: str) -> "Rule":
        if ":" not in s:
            return UnconditionalRule(s)

        cond, result = s.split(":")

        if "<" in cond:
            var, value = cond.split("<")
            op = "<"
        elif ">" in cond:
            var, value = cond.split(">")
            op = ">"
        else:
            assert False

        return ConditionRule(var, op, int(value), result.strip())


class ConditionRule(Rule):
    def __init__(self, var: str, op: str, value: int, if_true: str):
        self.var = var
        self.op = op
        self.value = value
        self.if_true = if_true

    def test(self, part: Part) -> Optional[str]:
        if self.op == ">":
            cond = part[self.var] > self.value
        elif self.op == "<":
            cond = part[self.var] < self.value
        else:
            assert False

        if cond:
            return self.if_true
        else:
            return None


class UnconditionalRule(Rule):
    def __init__(self, result: str):
        self.result = result

    def test(self, part: Part) -> Optional[str]:
        return self.result


class Workflow:
    def __init__(self, name: str, rules: List[Rule]):
        self.name = name
        self.rules = rules

    @staticmethod
    def parse(s: str) -> "Workflow":
        name, rules = s.split("{")
        rules = rules[:-1]
        name = name.strip()
        rules = [Rule.parse(rule.strip()) for rule in rules.split(",")]
        return Workflow(name, rules)

    def test(self, part: Part):
        for rule in self.rules:
            if (result := rule.test(part)) is not None:
                return result
        return None


class Pipeline:
    def __init__(self, workflows: List[Workflow]):
        self.workflows = {}
        for workflow in workflows:
            self.workflows[workflow.name] = workflow

    @staticmethod
    def read() -> "Pipeline":
        workflows = []
        while (line := sys.stdin.readline().strip()) != "":
            workflows.append(Workflow.parse(line))

        return Pipeline(workflows)

    def test(self, part):
        wf = self.workflows["in"]
        while (result := wf.test(part)) not in ["A", "R"]:
            wf = self.workflows[result]
        return result


pipeline = Pipeline.read()
parts = read_parts()

s = 0
for part in parts:
    accepted = pipeline.test(part) == "A"
    if accepted:
        s += part["x"] + part["m"] + part["a"] + part["s"]
print(s)
