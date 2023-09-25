import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("-u", "--usaco", action="store_true")
parser.add_argument("-f")
args = parser.parse_args()
with open(f"template/{'usaco' if args.usaco else 'normal'}.cpp") as f:
    template = f.read()
with open(f"{args.name}/{args.name}.cpp", "w") as f:
    f.write(template.replace("{problem name}", args.name))