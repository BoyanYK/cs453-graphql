import ast
import astor


class profiler_vistor(ast.NodeVisitor):
    def __init__(self):
        a = 0


class profiler_transformer(ast.NodeTransformer):
    def __init__(self):
        a = 0

    def insert_CustomFunction(self, node):
        new_node = ast.Expr(value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),
            args=[ast.Str(s=str("----REACHED-----"))],
            keywords=[]
        ))
        node.body.insert(0, new_node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.insert_CustomFunction(node)
        ast.NodeTransformer.generic_visit(self, node)
        # print(astor.dump_tree(node))
        return ast.fix_missing_locations(node)


def main():
    fname = "schema.py"
    with open(fname, "r") as source:
        tree = ast.parse(source.read())

    y = profiler_transformer()
    y.visit(tree)
    compile(tree, fname, 'exec')
    print("\n")

    print(astor.to_source(tree))




if __name__ == '__main__':
    main()
