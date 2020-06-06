import ast
import astor
from fitness import fitness_pred
from execution import Node


class ResolverInstrumentation(ast.NodeTransformer):
    def __init__(self, target, path, function_name="test_me"):
        self.target = target
        self.path = path
        self.function_name = function_name
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * TypeDef: FunctionDef(identifier name, arguments args,
        # *             stmt* body, expr* decorator_list, expr? returns,
        # *             string? type_comment)
        if node.name == self.function_name:
            trace = ast.parse("trace = []")
            context_add = ast.parse("info.context[\"trace_execution\"] = trace")
        self.generic_visit(node)
        return node, trace, context_add

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        state = self.path[Node(node)]
        branch_distance = __branch_dist(node.test, state)

        # TODO Add more logging attributes
        tracing = ast.parse("trace.append({})".format(branch_distance)).body[0]
        return tracing, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        state = self.path[Node(node)]
        branch_distance = __branch_dist(node.test, state)

        # TODO Add more logging attributes
        tracing = ast.parse("trace.append({})".format(branch_distance)).body[0]
        return tracing, node

    @staticmethod
    def __branch_dist(comp: ast.Compare, state, K=1):
        left = comp.left
        right = comp.comparators[0]
        pred = comp.ops[0]
        if not state:
            # * We just have to flip the values
            left, right = right, left

        if isinstance(pred, ast.Eq):
            return "abs({left} - {right})".format(left=left, right=right)
        elif isinstance(pred, ast.NotEq):
            return "-abs({left} - {right})".format(left=left, right=right)
        elif isinstance(pred, ast.Lt) or isinstance(pred, ast.LtE):
            return "{left} - {right} + {K}".format(left=left, right=right, K=K)
        elif isinstance(pred, ast.Gt) or isinstance(pred, ast.GtE):
            return "{right} - {left} + {K}".format(left=left, right=right, K=K)

