# TODO: checks (additional constraints for the objects, for example {int n [1, 10] check(n & 1) check(n > 5)s)})
# TODO: support for comments
from .exceptions import *
from .objects import *
import re
from inspect import signature
from typing import overload

__all__ = ["Parser"]

name = r"(?P<name>\w+)"
len_grp = r"(?P<len>\w+)"
case = r"(?P<case>lower|upper)"
rng = r"\[\s*(?P<l>.+?)\s*(?:,\s*(?P<r>.+?)\s*)?\]"

class Parser:
    _op = re.compile(r"{[^}]+}")
    operations = [
        re.compile(rf"(?P<op>char)\s+{name}\s*{case}?"),
        re.compile(rf"(?P<op>str)\s+{name}\s*{case}?\s*{rng}"),
        re.compile(rf"(?P<op>int|float)\s+(?P<n>\w+)\s*{rng}"),
        re.compile(rf"(?P<op>arr)\s+{len_grp}\s+(?P<type>.+)"),
        re.compile(r"(?P<op>eval)\s+(?P<expr>.+)"),
        re.compile(rf"(?P<op>tree)\s+{name}\s*{len_grp}")
    ]
    controls = [
        re.compile(r"(?P<ctrl>loop)\s+(?P<var>\w+)"),
        re.compile(r"(?P<ctrl>if)\s+(?P<cond>.+)"),
        re.compile(r"(?P<ctrl>exec)")
    ]

    def __init__(self, code: list[str] | str):
        if isinstance(code, str): code = code.split("\n")
        self.code = code
        self.pos = 0

    @staticmethod
    def get_indent(x: str) -> int:
        indent = re.match(r"\s+", x)
        if indent: return (indent.end() - indent.start())
        else: return 0

    def parse_int(self, m: re.Match) -> Integer:
        return Integer(m["n"], m["l"], m["r"])

    def parse_float(self, m: re.Match) -> Float:
        return Float(m["n"], m["l"], m["r"])

    def parse_char(self, m: re.Match) -> Char:
        case = m["case"]
        if case not in ("lower", "upper"): case = None
        return Char(m["name"], Case(case))

    def parse_str(self, m: re.Match) -> String:
        case = m["case"]
        if case not in ("lower", "upper"): case = None
        return String(m["name"], Case(case), m["l"], m["r"])

    def parse_arr(self, m: re.Match) -> Array:
        op = self.parse_op(m["type"])
        if not op:
            raise UnknownStatement()
        return Array(m["len"], op)

    def parse_tree(self, m: re.Match) -> Tree:
        return Tree(m["name"], m["len"])

    def parse_eval(self, m: re.Match) -> Eval:
        expr = m["expr"].strip()
        if not expr:
            raise SyntaxError("Expression for eval operation is empty")
        return Eval(expr)

    def parse_exec(self, m: re.Match, till: int) -> Eval:
        code = ""
        indent = self.get_indent(self.code[self.pos])
        for i in range(self.pos, till):
            code += self.code[i][indent:] + "\n"
        ret = Eval(code.strip())
        self.pos = till+1
        return ret

    def parse_loop(self, m: re.Match, till: int) -> Loop:
        try:
            return Loop(m["var"], self.parse(till))
        except SyntaxError as e:
            lines: list[str] = e.args[0].split('\n')
            raise SyntaxError(lines[0].split(': ', 1)[1] + "\n" + "\n".join(lines[1:]))

    def parse_if(self, match: re.Match, till: int, indent: int) -> If:
        i = self.pos+1
        code = None
        blocks = []
        prev_cond = None
        blocks_finished = False
        while i < till:
            m = re.fullmatch(" "*indent + r"{else(\s*if\s+(?P<cond>[^}]+))?}", self.code[i])
            if m:
                if blocks_finished:
                    raise SyntaxError("There is an else/else if statement after an else statement")
                if not m["cond"]:
                    blocks_finished = True
                if not code:
                    code = self.parse(i)
                else:
                    blocks.append(IfBlock(self.parse(i), prev_cond))
                self.pos += 1
                prev_cond = m["cond"]
            i += 1
        if not code:
            code = self.parse(till)
        else: blocks.append(IfBlock(self.parse(i), prev_cond))
        return If(code, match["cond"], blocks)

    def parse_op(self, op: str) ->  Value | None:
        for p in self.operations:
            m = re.fullmatch(p, op)
            if m:
                method = getattr(self, f"parse_{m['op']}", None)
                if not method:
                    raise NotImplementedError(f"Parse method for \"{m['op']}\" has not been implemented yet")
                return method(m)

    def parse_ctrl(self, ctrl: str, indent: int) -> ControlFlow | None:
        for p in self.controls:
            m = re.fullmatch(p, ctrl)
            if m:
                method = getattr(self, f"parse_{m['ctrl']}", None)
                if not method:
                    raise NotImplementedError(f"Parse method for \"{m['ctrl']}\" has not been implemented yet")
                self.pos += 1
                till = self.pos
                while (till < len(self.code) and self.code[till] != (" "*indent + "{end}")):
                    till += 1
                if (till == len(self.code)):
                    raise EOFError(f"Control \"{m['ctrl']}\" has not been ended")
                if "indent" in signature(method).parameters.keys(): return method(m, till, indent)
                else: return method(m, till)

    def parse(self, till: int | None = None) -> list[list[Object]]:
        till = till or len(self.code)
        ret: list[list[Object]] = []
        while self.pos < till:
            curr = []
            line = self.code[self.pos].strip()
            if not line:
                self.pos += 1
                continue
            ops = re.findall(self._op, line)
            if not ops and line:
                raise SyntaxError(f"Invalid Syntax on line {self.pos+1}: Unknown Statement\n\t{line}")
            indent = self.get_indent(self.code[self.pos])
            for op in ops:
                try:
                    parsed = self.parse_op(op[1:-1])
                    if not parsed:
                        parsed = self.parse_ctrl(op[1:-1], indent)
                        if not parsed:
                            raise UnknownStatement()
                    curr.append(parsed)
                except Exception as e:
                    raise SyntaxError(f"Invalid Syntax on line {self.pos+1}: {e.args[0]}\n\t{op[1:-1]}")
            ret.append(curr)
            self.pos += 1
        return ret