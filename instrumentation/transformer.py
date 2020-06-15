import ast
import astor
import copy
from instrumentation.execution import Node


class ResolverInstrumentation(ast.NodeTransformer):
    def __init__(self, target, path, function_name="test_me"):
        self.target = target
        self.path = copy.deepcopy(path)
        self.function_name = function_name

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * TypeDef: FunctionDef(identifier name, arguments args,
        # *             stmt* body, expr* decorator_list, expr? returns,
        # *             string? type_comment)
        # If this is the correct target function:
        # Add a new line to the body of the function that will contain the execution trace as part of the 
        # GraphQL context object
        if node.name == self.function_name:
            context_add = ast.parse("info.context[\"trace_execution\"] = []").body[0]
            
            node.body = [context_add] + node.body
            self.generic_visit(node)
            return node
        else:
            self.generic_visit(node)
            return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        # Try to 'pop' node from expected path. If it exists then:
        # 1. Get a string form expression for calculating the branch distance given a target state (T/F) and the IF predicate
        # 2. To the execution trace, add a tuple consisting of (expr.name, predicate.value, lineno, branch_distance), where expression name
        # would be IF and the predicate value is calculated depending on the variables within it
        # 3. Put this execution trace update BEFORE the IF statement - guarantees its going to be executed (if we get to this branch)
        custom_node = Node(node)
        state = self.path.pop(custom_node, None)
        if state != None:
            branch_distance = ResolverInstrumentation.__branch_dist(
                node.test, state)

            context_add = ast.parse(
                "info.context[\"trace_execution\"].append((\"{node}\", {test}, {lineno}, {bd}))".format(
                node=node.__class__.__name__, test=astor.to_source(node.test), lineno=node.lineno, bd=branch_distance)).body[0] 

            self.generic_visit(node)
            return context_add, node
        else:
            self.generic_visit(node)
            return node

    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
         # Try to 'pop' node from expected path. If it exists then:
        # 1. Get a string form expression for calculating the branch distance given a target state (T/F) and the WHILE predicate
        # 2. To the execution trace, add a tuple consisting of (expr.name, predicate.value, lineno, branch_distance), where expression name
        # would be WHILE and the predicate value is calculated depending on the variables within it
        # 3. Put this execution trace update BEFORE the WHILE statement - guarantees its going to be executed (if we get to this branch)
        custom_node = Node(node)
        state = self.path.pop(custom_node, None)
        if state != None:
            branch_distance = ResolverInstrumentation.__branch_dist(
                node.test, state)

            context_add = ast.parse(
                "info.context[\"trace_execution\"].append((\"{node}\", {test}, {lineno}, {bd}))".format(
                node=node.__class__.__name__, test=astor.to_source(node.test), lineno=node.lineno, bd=branch_distance)).body[0] 
                
            self.generic_visit(node)
            return context_add, node
        else:
            self.generic_visit(node)
            return node

    @staticmethod
    def __branch_dist(comp: ast.Compare, state: bool, K=1):
        """[summary]
        Return a string form of the branch distance calculation given an AST comparator object and a target state
        Handles Unary, Boolean and Comparison operations
        Args:
            comp (ast.Compare): Predicate of IF/WHILE branch
            state (bool): Target state of the given expression
            K (int, optional): [description]. Defaults to 1.

        Returns:
            str: String form of branch distance expression calculation
        """
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
