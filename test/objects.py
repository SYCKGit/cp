from __future__ import annotations
from .exceptions import *

import random, string, heapq
from abc import ABC, abstractmethod
from enum import Enum
from inspect import signature
from typing import Any, Union

__all__ = (
    "Object",
    "Value",
    "Integer",
    "Float",
    "Case",
    "Char",
    "String",
    "Array",
    "Tree",
    "Eval",
    "ControlFlow",
    "Loop",
    "IfBlock",
    "If"
)

class Object(ABC):
    @abstractmethod
    def generate(self, *, values: dict[str, Any]):
        raise NotImplementedError(f"{self.__class__.__name__} generation has not been implemented yet")

# VALUES
class Value(Object):
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __repr__(self) -> str:
        return str(self)

def get_range(values: dict[str, Any], sl: str, sr: str | None = None) -> tuple[int, int]:
    l = int(eval(sl, globals(), values))
    r = l
    if sr: r = int(eval(sr, globals(), values))
    return l, r

class Integer(Value):
    def __init__(self, name: str, l: str, r: str | None = None):
        super().__init__(name)
        self.l = l
        self.r = r

    def generate(self, *, values) -> int:
        l, r = get_range(values, self.l, self.r)
        return random.randint(l, r)

    def __str__(self):
        return f"Integer({self.name} [{self.l}, {self.r}])"

class Float(Value):
    def __init__(self, name: str, l: str, r: str | None = None):
        super().__init__(name)
        self.l = l
        self.r = r

    def generate(self, *, values) -> float:
        l, r = get_range(values, self.l, self.r)
        return l + random.random() * (r-l)

class Case(Enum):
    none = None
    lower = "lower"
    upper = "upper"

class TextType(Value):
    def __init__(self, name: str, case: Case):
        super().__init__(name)
        assert isinstance(case, Case), f"case argument is not an instance of Case ({case})"
        self.case: Case = case

    def getch(self) -> str:
        assert isinstance(self.case, Case), f"case argument is not an instance of Case ({self.case})"
        if self.case is Case.lower:
            return random.choice(string.ascii_lowercase)
        elif self.case is Case.upper:
            return random.choice(string.ascii_uppercase)
        else:
            return random.choice(string.ascii_letters)

class Char(TextType):
    def generate(self, *, values) -> str:
        return self.getch()

class String(TextType):
    def __init__(self, name: str, case: Case, l: str, r: str | None = None):
        super().__init__(name, case)
        self.l = l
        self.r = r

    def generate(self, *, values) -> str:
        l, r = get_range(values, self.l, self.r)
        return "".join(self.getch() for _ in range(random.randint(l, r)))

class Array(Value):
    def __init__(self, length: str, type: Value):
        self.type = type
        self.length = length
        super().__init__(type.name)

    def generate(self, *, values) -> list[Any]:
        ret = []
        try:
            length = values[self.length]
        except KeyError:
            raise UnknownIdentifier(self.length)
        for _ in range(length):
            ret.append(self.type.generate(values=values))
        return ret

class Tree(Value):
    def __init__(self, name: str, length: str):
        super().__init__(name)
        self.length = length

    def generate(self, *, values) -> list[list[int]]:
        n = eval(self.length, globals(), values)
        prufer = [random.randint(1, n) for _ in range(n-2)]
        left = [0] * (n+1)
        for i in prufer:
            left[i] += 1
        pq: list[int] = []
        for i in range(1, n+1):
            if left[i] == 0:
                heapq.heappush(pq, i)
        res = []
        for i in prufer:
            res.append([heapq.heappop(pq), i])
            left[i] -= 1
            if left[i] == 0:
                heapq.heappush(pq, i)
        res.append([heapq.heappop(pq), heapq.heappop(pq)])
        return res

# OBJECTS
class Eval(Object):
    def __init__(self, code: str):
        self.code = code

    def generate(self, *, values) -> Any:
        return exec(self.code, globals(), values)

# CONTROL FLOWS
class ControlFlow(Object):
    def __init__(self, code: list[list[Object]]):
        self.code = code

    def generate(self, *, values) -> list[list[Any]]:
        ret = []
        for line in self.code:
            curr = []
            for op in line:
                val = op.generate(values=values)
                if isinstance(op, (Value, ControlFlow)):
                    curr.append(val)
                if isinstance(op, Value):
                    values[op.name] = val
            if curr:
                ret.append(curr)
        return ret

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(map(repr, self.code))})"

    def __repr__(self) -> str:
        return str(self)

class Loop(ControlFlow):
    def __init__(self, var: str, code: list[list[Object]]):
        super().__init__(code)
        self.var = var

    def generate(self, *, values: dict[str, Any]) -> list[list[Any]]:
        try:
            var = values[self.var]
        except KeyError:
            raise UnknownIdentifier(self.var)
        ret = []
        for _ in range(var):
            ret.extend(super().generate(values=values))
        return ret

class IfBlock(ControlFlow):
    def __init__(self, code: list[list[Object]],  cond: str | None = None):
        super().__init__(code)
        self.cond = cond

class If(ControlFlow):
    def __init__(self, code: list[list[Object]], cond: str, blocks: list[IfBlock]):
        super().__init__(code)
        self.blocks = blocks
        self.cond: str = cond

    def generate(self, *, values: dict[str, Any]):
        if eval(self.cond, globals(), values):
            return super().generate(values=values)
        for block in self.blocks:
            if (not block.cond) or eval(block.cond, globals(), values):
                return block.generate(values=values)