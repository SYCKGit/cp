from __future__ import annotations
from .exceptions import *

import random, string
from abc import ABC, abstractmethod
from enum import Enum
from inspect import signature
from typing import Any, Union

__all__ = (
    "input_type",
    "Object",
    "Integer",
    "Float",
    "Case",
    "Char",
    "String",
    "Array",
    "ControlFlow",
    "Loop",
    "IfBlock",
    "If"
)

input_type = Union['Object', 'ControlFlow']

# OBJECTS
class Object(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def generate(self, *, values: dict[str, Any]):
        raise NotImplementedError(f"{self.__class__.__name__} generation has not been implemented yet")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"

    def __repr__(self) -> str:
        return str(self)

class Integer(Object):
    def __init__(self, name: str, l: int, r: int):
        super().__init__(name)
        self.l: int = l
        self.r: int = r

    def generate(self) -> int:
        return random.randint(self.l, self.r)

    def __str__(self):
        return f"Integer({self.name} [{self.l}, {self.r}])"

class Float(Object):
    def __init__(self, name: str, l: int, r: int):
        super().__init__(name)
        self.l = l
        self.r = r

    def generate(self) -> float:
        return self.l + random.random() * (self.r-self.l)

class Case(Enum):
    none = None
    lower = "lower"
    upper = "upper"

class TextType(Object):
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
    def generate(self) -> str:
        return self.getch()

class String(TextType):
    def __init__(self, name: str, case: Case, l: int | None, r: int):
        super().__init__(name, case)
        self.length: range | int = r
        if l:
            self.length = range(l, r+1)

    def generate(self) -> str:
        l = self.length
        if isinstance(l, range):
            l = random.randrange(l.start, l.stop)
        return "".join(self.getch() for _ in range(l))

class Array(Object):
    def __init__(self, length: str, type: Object):
        self.type = type
        self.length = length
        super().__init__(type.name)

    def generate(self, *, values: dict[str, Any]) -> list[Any]:
        ret = []
        try:
            length = values[self.length]
        except KeyError:
            raise UnknownIdentifier(self.length)
        for _ in range(length):
            ret.append(self.type.generate())
        return ret

# CONTROL FLOWS
class ControlFlow(ABC):
    def __init__(self, code: list[list[input_type]]):
        self.code = code

    def generate(self, *, values: dict[str, Any]) -> list[list[Any]]:
        ret = []
        for line in self.code:
            curr = []
            for op in line:
                if "values" in signature(op.generate).parameters:
                    val = op.generate(values=values)
                else: val = op.generate()
                curr.append(val)
                if isinstance(op, Object):
                    values[op.name] = val
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
    def __init__(self, code: list[list[input_type]],  cond: str | None = None):
        super().__init__(code)
        self.cond = cond

class If(ControlFlow):
    def __init__(self, code: list[list[input_type]], cond: str, blocks: list[IfBlock]):
        super().__init__(code)
        self.blocks = blocks
        self.cond: str = cond

    def generate(self, *, values):
        if eval(self.cond, globals(), values):
            return super().generate(values=values)
        for block in self.blocks:
            if (not block.cond) or eval(block.cond, globals(), values):
                return block.generate(values=values)