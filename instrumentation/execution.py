import ast

class Node(object):
    def __init__(self, node, branch_value=None, parent=None):
        self.name = node.__class__.__name__
        self.parent = parent
        self.depth = 0 if not self.parent else self.parent.depth +  1
        self.lineno = node.lineno
        self.node = node
        self.branch_value = branch_value
        self.children = []

    def __str__(self):
        return "{} @ Line {}".format(self.name, self.lineno)

    def get_body(self):
        try:
            return self.node.body
        except Exception:
            return []

    def get_else(self):
        try:
            return self.node.orelse
        except Exception:
            return []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return self.__str__()

    def compare(self, target):
        return self.name == target[0] and self.lineno == target[3]

def get_control_nodes(tree, func_name="test_me"):
    arg_count = 0
    # * We first search for the target function within all nodes of the file
    # * And save it as an initial node
    tree_nodes = tree.body
    for stmt in tree_nodes:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == func_name:
            function = Node(stmt, 0)
            arg_count = len(stmt.args.args)
            break
        try:
            tree_nodes += stmt.body
        except AttributeError:
            pass
        
    queue = []
    queue.append(function)
    flow_change = []
    while queue:
        node = queue.pop(0)
        for child in node.get_body():
            child_node = Node(child, branch_value=True, parent=node)
            queue.append(child_node)
            node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While) or isinstance(node.node, ast.For):
            for child in node.get_else():
                child_node = Node(child, branch_value=False, parent=node)
                queue.append(child_node)
                node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):
            flow_change.append(node)
    return function, flow_change, arg_count