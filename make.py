import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("-u", "--usaco", action="store_true")
parser.add_argument("-b", "--bare", action="store_true")
parser.add_argument("-f", action="store_true")
args = parser.parse_args()

with open(f"template/full/{(args.usaco and 'usaco') or (args.bare and 'bare') or 'normal'}.cpp") as f:
    template = f.read()
with open(f"{args.name}/{args.name}.cpp", "w") as f:
    f.write(template.replace("{problem name}", args.name))