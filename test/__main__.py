# TODO: Implement auto template generator
# TODO: Implement random auto checker
from .parser import Parser
from .generator import Generator
from argparse import ArgumentParser
from os.path import isdir

def problem(pname: str):
    if isdir(pname):
        return pname
    else:
        raise NotADirectoryError(pname)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("PROBLEM_NAME", type=problem)
    args = parser.parse_args()
    with open(f"{args.PROBLEM_NAME}/fmt.in") as f:
        try:
            with open(f"{args.PROBLEM_NAME}/{args.PROBLEM_NAME}.in", "w") as p:
                p.write(Generator(Parser(f.read())).generate())
        except Exception as e:
            print(f"SyntaxError: {e}")