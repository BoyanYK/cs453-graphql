import ast
import astor
import copy
from search import avm
from instrumentation.transformer import ResolverInstrumentation
from instrumentation.execution import get_targets

def do_search(schema: ast.Module, targets: dict, args=1, target_func="resolve_char"):
    """[summary]

    Args:
        schema (ast.Module): Python Graphene schema file parsed as an AST object
        targets (dict): Targets dict of the form {target: path}. Path is another dict of the form {node: state}
        args (int, optional): How many arguments the function takes. Defaults to 1.
        target_func (str, optional): Name of the target function. Defaults to "resolve_char".
    """
    results = {}
    for target, path in targets.items():
        # * Each target can have a True and a False state
        print(target, path)
        for state in [True, False]:
            schema_copy = copy.deepcopy(schema)
            path[target] = state
            instrumentation = ResolverInstrumentation(target, path, target_func)
            instrumented_schema = instrumentation.visit(schema_copy)

            avm_search = avm.AVM(instrumented_schema, path, args, state, target_func)
            result = avm_search.search()

            results[(target, state)] = result

    for (target, state), (inputs, value) in results.items():
        print("Target {} @ state {} with inputs {}".format(target, state, inputs))

def run(schema_path: str):
    """[summary]
    Parse python schema file 
    Generate copy of the AST (just in case)
    Find all branches within the tree
    Execute search on the tree with the found targets
    Args:
        schema_path (str): Path to python schema file
    """
    schema_tree = astor.parse_file(schema_path)
    copy_schema_tree = copy.deepcopy(schema_tree)
    targets = get_targets(copy_schema_tree)
    do_search(schema_tree, targets)

