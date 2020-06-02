import ast
import astor

class profiler_vistor(ast.NodeVisitor):
    def __init__(self):
        a=0

def main():
    fname = "schema.py"
    with open(fname, "r") as source:
        tree = ast.parse(source.read())

    print(astor.dump_tree(tree))

if __name__ == '__main__':
    main()