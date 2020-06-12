import ast
import copy, sys
from graphene.test import Client

from starwars.data import setup as swsetup
from harrypotter.data import setup as hpsetup
from starwars.schema import schema as schema

from search.utils import blockPrint, enablePrint

class Node(object):
    """
    This is a custom object that serves as a helper container when building up the AST
    in a custom form.
    """
    def __init__(self, node, branch_value=None, parent=None):
        """Basic constructor

        Args:
            node (ast.Node): Python AST Node that we are creating a wrapper for
            branch_value (bool, optional): The branch value of the parent node. Helps with finding the tree path to this node. Defaults to None.
            parent (ast.Node, optional): Parent node. Defaults to None.
        """
        self.name = node.__class__.__name__
        self.parent = parent
        self.depth = 0 if not self.parent else self.parent.depth +  1
        self.lineno = node.lineno
        self.node = node
        self.branch_value = branch_value
        self.children = []

    def __str__(self):
        return "{} @ Line {}".format(self.name, self.lineno, self.branch_value)

    def get_body(self):
        """
        This function is used to return the children on the true branch of a node , if it has any.
        Returns:
            list: [True] Children nodes, if any
        """
        try:
            return self.node.body
        except Exception:
            return []

    def get_else(self):
        """[summary]
        This function is used to return the children on the false branch of a node , if it has any.
        Returns:
            list: [False] Children nodes, if any
        """
        try:
            return self.node.orelse
        except Exception:
            return []

    def add_child(self, child):
        """[summary]
        Add child object to this node. Not really used.
        Args:
            child (ast.Node): Child to append to children list
        """
        self.children.append(child)

    def __repr__(self):
        return self.__str__()

    def compare(self, target):
        """[summary]
        Functions is used to compare whether a part of the executed trace corresponds to a Node object from the expected path.
        Args:
            target (Path tuple object): Tuple representing part/node of the executed path

        Returns:
            bool: Whether or node it is the same expression
        """
        return self.name == target[0] and self.lineno == target[2]

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
    
    # * Create Queue for BFS-style iteration
    queue = []
    queue.append(function)
    # * List to store nodes that impact the flow of the program
    flow_change = []
    while queue:
        node = queue.pop(0)
        # * Add True branch children nodes
        for child in node.get_body():
            branch_value = None
            if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):
                branch_value = True
            child_node = Node(child, branch_value=branch_value, parent=node)
            queue.append(child_node)
            node.add_child(child_node)

        # * Add False branch children nodes
        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While) or isinstance(node.node, ast.For):
            for child in node.get_else():
                child_node = Node(child, branch_value=False, parent=node)
                queue.append(child_node)
                node.add_child(child_node)

        # * Add If and While nodes to flow change list
        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):
            flow_change.append(node)
    return function, flow_change

def get_targets(tree, func_name="resolve_char"):
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

def wrap_schema(instrumented_tree):
    """[summary]
    This function takes the branch-distance instrumented schema and wraps it around another function such that we can 
    return the schema object instance as python object to run 
    Args:
        instrumented_tree (ast.Module): AST of schema file with modifications for branch distance already done

    Returns:
        ast.Module: AST that upon execution would return the schema as a python executable object
    """
    wrapper = ast.FunctionDef(name='wrapper_function',
                              args=ast.arguments(posonlyargs=[], args=[], vararg=None,
                                                 kwonlyargs=[],
                                                 kw_defaults=[],
                                                 kwarg=None,
                                                 defaults=[]), decorator_list=[], returns=None, type_comment=None)
    wrapper.body = [*instrumented_tree.body, ast.parse("return schema").body[0]]
    instrumented_tree.body = [wrapper]
    ast.fix_missing_locations(instrumented_tree)
    return instrumented_tree

def executable_schema(instrumented_tree):
    """[summary]
    Given an instrumented AST of the schema file, returns the schema as an object to execute (rather than an AST one)
    Args:
        instrumented_tree (ast.Module): AST of schema file with modifications for branch distance already done

    Returns:
        schema: Schema to run queries and mutations against
    """
    copy_tree = copy.deepcopy(instrumented_tree)
    exec_tree = wrap_schema(copy_tree)
    exec_schema = compile(exec_tree, filename='schema_2', mode='exec')
    namespace = {}
    sys.path.append('./')
    exec(exec_schema, namespace)
    return namespace['wrapper_function']()

def run_test(instrumented_schema, query, params):
    """[summary]

    Args:
        instrumented_schema (ast.Module): The AST form of the instrumented schema.py file
        query (string): GraphQL query string for target function
        params (list): List of arguments to be passed to the query

    Returns:
        list(tuple): List of tuples representing the executed path/trace. Format is (expr, test_val, lineno, branch_dist)
    """
    schema = executable_schema(instrumented_schema)
    swsetup()
    hpsetup()
    client = Client(schema)
    context = {"trace_execution": []}
    params = {"someId": str(params[0])}

    blockPrint()
    client.execute(query, context=context, variables=params)
    enablePrint()

    exec_path = context["trace_execution"]
    return exec_path


