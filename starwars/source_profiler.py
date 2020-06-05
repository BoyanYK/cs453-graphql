import ast
import astor
import logging
import copy

import graphene
from graphene.test import Client


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
        return ast.fix_missing_locations(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.insert_CustomFunction(node)
        ast.NodeTransformer.generic_visit(self, node)
        # print(astor.dump_tree(node))
        return ast.fix_missing_locations(node)


def convertExpr2Expression(Expr):
    Expr.lineno = 0
    Expr.col_offset = 0
    result = ast.Expression(Expr.value, lineno=0, col_offset=0)

    return result


def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]
    # print(astor.dump_tree(init_ast.body))

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"), globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"), globals())


def wrap_function(tree, args, func_name="test_me"):
    wrapper = ast.FunctionDef(name='wrapper',
    args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='trace', annotation=None, type_comment=None)], vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]), decorator_list=[], returns=None, type_comment=None)
    target_call = func_name + '('
    for arg in args:
        target_call += str(arg) + ', '
    target_call += 'trace)'
    call = ast.parse(target_call)
    wrapper.body = [*tree.body, call.body[0]]
    tree.body = [wrapper]
    ast.fix_missing_locations(tree)
    return tree


def main():
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.setLevel(logging.INFO)
    log.addHandler(console)

    # fname = "schema.py"
    # with open(fname, "r") as source:
    #     tree = ast.parse(source.read())
    import starwars.schema as schema
    tree = astor.code_to_ast(schema)
    # print(tree)

    # TODO
    y = profiler_transformer()
    y.visit(tree)
    # compile(tree, "fname", 'exec')

    schema = compile(tree, "schema.py", "exec")
    print(astor.dump_tree(schema))

    # a = exec_with_return(schema)
    #
    # print(a)

    ##this doesnt work because client expects a schema instance
    # but schema is now defiined as a ast.module object
    # client = Client(schema)
    # query = """
    #     query FetchSomeIDQuery($someId: String!) {
    #       human(id: $someId) {
    #         name
    #       }
    #     }
    # """
    # params = {"someId": "3000"}
    # print(client.execute(query, variables=params))

    # log.info(astor.to_source(tree))


if __name__ == '__main__':
    main()
