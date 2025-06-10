from .parser import Parser
from .objects import *
from .exceptions import *
from inspect import signature

class Generator():
    def __init__(self, code: list[list[Object]] | Parser):
        if isinstance(code, Parser):
            code = code.parse()
        self.code: list[list[Object]] = code

    @staticmethod
    def value_to_str(v):
        if isinstance(v, list):
            return " ".join(map(Generator.value_to_str, v))
        return str(v)

    @staticmethod
    def ctrl_to_str(l):
        ret = ""
        for line in l:
            for op in line:
                if isinstance(op, list):
                    if isinstance(op[0], list):
                        if ret[-1] != '\n': ret += '\n'
                        ret += Generator.ctrl_to_str(op)[:-1]
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
                val = op.generate(values=values)
                if isinstance(op, Value):
                    values[op.name] = val
                    curr += self.value_to_str(val) + " "
                elif isinstance(op, ControlFlow):
                    if curr:
                        ret += curr.strip() + "\n"
                        curr = ""
                    ret += self.ctrl_to_str(val)[:-1] + "\n"
            if curr:
                ret += curr.strip() + "\n"
        return ret