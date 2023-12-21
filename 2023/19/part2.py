from dataclasses import dataclass
import sys
from typing import List, Optional


@dataclass
class Condition:
    var: str
    op: str
    value: int

    def negate(self):
        if self.op == "<":
            return Condition(self.var, ">=", self.value)
        elif self.op == ">":
            return Condition(self.var, "<=", self.value)
        else:
            assert False

    def intersect_range(self, fro: int, to: int) -> tuple[int, int]:
        if self.op == "<":
            return (fro, min(to, self.value - 1))
        elif self.op == ">":
            return (max(fro, self.value + 1), to)
        elif self.op == "<=":
            return (fro, min(to, self.value))
        elif self.op == ">=":
            return (max(fro, self.value), to)
        else:
            assert False


class AcceptableRanges:
    def __init__(self, ranges: dict[str, tuple[int, int]]):
        self.ranges = ranges

    def merge(self, condition: Condition) -> "AcceptableRanges":
        new_ranges = self.ranges.copy()
        new_ranges[condition.var] = condition.intersect_range(
            self.ranges[condition.var][0], self.ranges[condition.var][1]
        )
        return AcceptableRanges(new_ranges)

    def num_options(self) -> int:
        num_options = 1
        for var in self.ranges:
            num_options *= self.ranges[var][1] - self.ranges[var][0] + 1
        return num_options


class Rule:
    def __init__(self, condition: Optional[Condition], if_true: str):
        self.condition = condition
        self.if_true = if_true

    @staticmethod
    def parse(s: str) -> "Rule":
        if ":" not in s:
            return Rule(None, s)

        cond, result = s.split(":")

        if "<" in cond:
            var, value = cond.split("<")
            condition = Condition(var, "<", int(value))
        elif ">" in cond:
            var, value = cond.split(">")
            condition = Condition(var, ">", int(value))
        else:
            assert False

        return Rule(condition, result.strip())


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

    def collect_accepts(self, name: str) -> List[AcceptableRanges]:
        if name == "A":
            return [
                AcceptableRanges(
                    {
                        "x": (1, 4000),
                        "m": (1, 4000),
                        "a": (1, 4000),
                        "s": (1, 4000),
                    }
                )
            ]
        elif name == "R":
            return []

        workflow = self.workflows[name]

        accepts: List[AcceptableRanges] = []
        prev_negations: List[Condition] = []
        for rule in workflow.rules:
            rule_accepts = self.collect_accepts(rule.if_true)

            for prev_neg in prev_negations:
                rule_accepts = [accept.merge(prev_neg) for accept in rule_accepts]

            if rule.condition:
                rule_accepts = [accept.merge(rule.condition) for accept in rule_accepts]
                prev_negations.append(rule.condition.negate())
            accepts.extend(rule_accepts)

        return accepts


pipeline = Pipeline.read()

s = 0
for ranges in pipeline.collect_accepts("in"):
    s += ranges.num_options()
print(s)
