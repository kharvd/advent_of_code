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


class UnconditionalRule(Rule):
    def __init__(self, if_true: str):
        self.if_true = if_true


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

    def collect_accepts(self, name: str) -> List[List[Condition]]:
        if name == "A":
            return [[]]
        elif name == "R":
            return []

        workflow = self.workflows[name]

        accepts: List[List[Condition]] = []
        prev_negations: List[Condition] = []
        for rule in workflow.rules:
            rule_accepts = self.collect_accepts(rule.if_true)
            curr_rule_condition = [rule.condition] if rule.condition else []
            accepts.extend(
                [
                    curr_rule_condition + prev_negations + accept
                    for accept in rule_accepts
                ]
            )
            if curr_rule_condition:
                prev_negations.append(rule.condition.negate())

        return accepts


def count_options(conditions: List[Condition]) -> int:
    var_ranges: dict[str, tuple[int, int]] = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    for condition in conditions:
        range = var_ranges[condition.var]
        var_ranges[condition.var] = condition.intersect_range(range[0], range[1])

    num_options = 1
    for var in var_ranges:
        num_options *= var_ranges[var][1] - var_ranges[var][0] + 1
    return num_options


pipeline = Pipeline.read()

s = 0
for ruleset in pipeline.collect_accepts("in"):
    s += count_options(ruleset)
print(s)
