from abc import ABC
from dataclasses import dataclass
import sys
from typing import List


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


class Rule(ABC):
    @staticmethod
    def parse(s: str) -> "Rule":
        if ":" not in s:
            return UnconditionalRule(s)

        cond, result = s.split(":")

        if "<" in cond:
            var, value = cond.split("<")
            condition = Condition(var, "<", int(value))
        elif ">" in cond:
            var, value = cond.split(">")
            condition = Condition(var, ">", int(value))
        else:
            assert False

        return ConditionRule(condition, result.strip())


class ConditionRule(Rule):
    def __init__(self, condition: Condition, if_true: str):
        self.condition = condition
        self.if_true = if_true


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
            return [
                [
                    Condition("x", ">=", 1),
                    Condition("x", "<=", 4000),
                    Condition("m", ">=", 1),
                    Condition("m", "<=", 4000),
                    Condition("a", ">=", 1),
                    Condition("a", "<=", 4000),
                    Condition("s", ">=", 1),
                    Condition("s", "<=", 4000),
                ]
            ]
        elif name == "R":
            return []

        workflow = self.workflows[name]

        accepts: List[List[Condition]] = []
        prev_negations: List[Condition] = []
        for rule in workflow.rules:
            if isinstance(rule, ConditionRule):
                rule_accepts = self.collect_accepts(rule.if_true)
                curr_accepts = [
                    [rule.condition] + prev_negations + accept
                    for accept in rule_accepts
                ]
                prev_negations.append(rule.condition.negate())
                accepts.extend(curr_accepts)
            elif isinstance(rule, UnconditionalRule):
                rule_accepts = self.collect_accepts(rule.if_true)
                accepts.extend([prev_negations + accept for accept in rule_accepts])

        return accepts


def count_options(conditions: List[Condition]) -> int:
    var_ranges = {
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
    }
    for condition in conditions:
        if condition.op == "<":
            var_ranges[condition.var][1] = min(
                var_ranges[condition.var][1], condition.value - 1
            )
        elif condition.op == ">":
            var_ranges[condition.var][0] = max(
                var_ranges[condition.var][0], condition.value + 1
            )
        elif condition.op == "<=":
            var_ranges[condition.var][1] = min(
                var_ranges[condition.var][1], condition.value
            )
        elif condition.op == ">=":
            var_ranges[condition.var][0] = max(
                var_ranges[condition.var][0], condition.value
            )
        else:
            assert False

    print(var_ranges)

    num_options = 1
    for var in var_ranges:
        num_options *= var_ranges[var][1] - var_ranges[var][0] + 1
    return num_options


pipeline = Pipeline.read()

s = 0
for ruleset in pipeline.collect_accepts("in"):
    s += count_options(ruleset)
print(s)
