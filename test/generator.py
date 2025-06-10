from .parser import Parser
from .objects import *
from .exceptions import *
from inspect import signature

class Generator():
    def __init__(self, code: list[list[input_type]] | Parser):
        if isinstance(code, Parser):
            code = code.parse()
        self.code: list[list[input_type]] = code

    @staticmethod
    def to_str(l):
        ret = ""
        for line in l:
            for op in line:
                if isinstance(op, list):
                    if isinstance(op[0], list):
                        if ret[-1] != '\n': ret += '\n'
                        ret += Generator.to_str(op)[:-1]
                    else:
                        ret += " ".join(map(str, op))
                else: ret += str(op) + " "
            ret = ret.strip() + "\n"
        return ret

    def generate(self) -> str:
        ret = ""
        values = {}
        for line in self.code:
            curr = ""
            for op in line:
                if "values" in signature(op.generate).parameters:
                    val = op.generate(values=values)
                else: val = op.generate() # type: ignore
                if isinstance(op, Value):
                    values[op.name] = val
                    curr += str(val) + " "
                elif isinstance(op, ControlFlow):
                    if curr:
                        ret += curr.strip() + "\n"
                        curr = ""
                    ret += self.to_str(val)[:-1] + "\n"
            if curr:
                ret += curr.strip() + "\n"
        return ret