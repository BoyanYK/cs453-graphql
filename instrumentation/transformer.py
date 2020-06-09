import ast
import astor
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
            context_add = ast.parse(
                "info.context[\"trace_execution\"] = trace")
            node.body = [trace, context_add] + node.body
            self.generic_visit(node)
            return node
        else:
            self.generic_visit(node)
            return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        custom_node = Node(node)
        state = self.path.pop(custom_node, None)
        if state != None:
            branch_distance = ResolverInstrumentation.__branch_dist(
                node.test, state)

            tracing = ast.parse("trace.append({node}, {test}, {lineno}, {bd})".format(
                node=node.__class__.__name__, test=astor.to_source(node.test), lineno=node.lineno, bd=branch_distance)).body[0]
            self.generic_visit(node)
            return tracing, node
        else:
            self.generic_visit(node)
            return node

    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        custom_node = Node(node)
        state = self.path.pop(custom_node, None)
        if state != None:
            branch_distance = ResolverInstrumentation.__branch_dist(
                node.test, state)

            tracing = ast.parse("trace.append({node}, {test}, {lineno}, {bd})".format(
                node=node.__class__.__name__, test=astor.to_source(node.test), lineno=node.lineno, bd=branch_distance)).body[0]
            self.generic_visit(node)
            return tracing, node
        else:
            self.generic_visit(node)
            return node

    @staticmethod
    def __branch_dist(comp: ast.Compare, state, K=1):
        if isinstance(comp, ast.Name):
            return "0 if {name} else {K}".format(name=astor.to_source(comp), K=K)

        if isinstance(comp, ast.UnaryOp):
            operation = comp.op
            if isinstance(operation, ast.Not):
                return "0 if not {name} else {K}".format(name=astor.to_source(comp), K=K)

        if isinstance(comp, ast.BoolOp):
            operation = comp.op
            if isinstance(operation, ast.And):
                return "{} + {}".format(ResolverInstrumentation.__branch_dist(comp.values[0], state), ResolverInstrumentation.__branch_dist(comp.values[1], state))
            elif isinstance(operation, ast.Or):
                return "min({}, {})".format(ResolverInstrumentation.__branch_dist(comp.values[0], state), ResolverInstrumentation.__branch_dist(comp.values[1], state))

        if isinstance(comp, ast.Compare):
            left = comp.left
            right = comp.comparators[0]
            pred = comp.ops[0]
            if not state:
                # * We just have to flip the values
                left, right = right, left

            if isinstance(pred, ast.Eq):
                return "abs({left} - {right})".format(left=astor.to_source(left), right=astor.to_source(right))
            elif isinstance(pred, ast.NotEq):
                return "-abs({left} - {right})".format(left=astor.to_source(left), right=astor.to_source(right))
            elif isinstance(pred, ast.Lt) or isinstance(pred, ast.LtE):
                return "{left} - {right} + {K}".format(left=astor.to_source(left), right=astor.to_source(right), K=K)
            elif isinstance(pred, ast.Gt) or isinstance(pred, ast.GtE):
                return "{right} - {left} + {K}".format(left=astor.to_source(left), right=astor.to_source(right), K=K)
