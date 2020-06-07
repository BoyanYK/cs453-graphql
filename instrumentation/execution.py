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
        return "{} @ Line {}, parent branch val {}".format(self.name, self.lineno, self.branch_value)

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

    def __eq__(self, target):
        return isinstance(target, Node) and self.name == target.name and self.lineno == target.lineno

    def __hash__(self):
        return hash((self.name, self.lineno))


def get_control_nodes(tree, func_name="test_me"):
    """[summary]
    Iterates the given module in a BFS fashion, searching for a given function name
    Generates a list of control nodes
    Args:
        tree (ast.Module): Tree to be traversed
        func_name (str, optional): [description]. Defaults to "test_me".

    Returns:
        ast.FunctionDef: Root node of target function
        list: List of all nodes that influence branching off
    """
    # * We first search for the target function within all nodes of the file
    # * And save it as an initial node
    tree_nodes = tree.body
    for stmt in tree_nodes:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == func_name:
            function = Node(stmt, None, None)
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
            branch_value = None
            if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):
                branch_value = True
            child_node = Node(child, branch_value=branch_value, parent=node)
            queue.append(child_node)
            node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While) or isinstance(node.node, ast.For):
            for child in node.get_else():
                child_node = Node(child, branch_value=False, parent=node)
                queue.append(child_node)
                node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):
            flow_change.append(node)
    return function, flow_change

def get_targets(tree, func_name="test_me"):
    """[summary]
    Given a (function) tree, get a dictionary of all target branches, along with the path to get there
    The path involves branch conditions for each parent branch
    Args:
        tree (ast.Module): Tree that is to be traversed
        func_name (str, optional): Function (name) to look for. Defaults to "test_me".

    Returns:
        dict: Target branches + execution path for each
    """
    root, flow_change  = get_control_nodes(tree, func_name)
    targets = {}
    for node in flow_change:
        node_tree = [node]
        path = {}
        iter_node = node
        while not isinstance(iter_node.parent.node, ast.FunctionDef):
            parent = iter_node.parent
            path[parent] = iter_node.branch_value
            node_tree.append(parent)
            iter_node = parent
        path[node] = None
        targets[node] = path
    return targets

    