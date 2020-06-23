import ast
import astor
import copy

from generator.query_gen import get_query_dict
from search import avm
from instrumentation.transformer import ResolverInstrumentation
from instrumentation.execution import get_targets
from search import randomsearch


def do_search(schema: ast.Module, targets: dict, strategy: str, target_func, query_str, field_args_dict, args=1):
    """[summary]

    Args:
        schema (ast.Module): Python Graphene schema file parsed as an AST object
        targets (dict): Targets dict of the form {target: path}. Path is another dict of the form {node: state}
        args (int, optional): How many arguments the function takes. Defaults to 1.
        target_func (str, optional): Name of the target function. Defaults to "resolve_char".
        strategy (str, optional): Search strategy to use, avm or random search. Args: (avm/rs), defaults to avm_gs.
    """
    results = {}
    for target, path in targets.items():
        # * Each target can have a True and a False state
        for state in [True, False]:
            schema_copy = copy.deepcopy(schema)
            path[target] = state
            instrumentation = ResolverInstrumentation(target, path, target_func)
            instrumented_schema = instrumentation.visit(schema_copy)

            if 'avm' in strategy:
                avm_search = avm.AVM(instrumented_schema, path, len(field_args_dict), state, target_func, query_str, field_args_dict)
                result = avm_search.search(method=strategy)

            elif strategy == 'rs':
                rs_search = randomsearch.RS(instrumented_schema, path, len(field_args_dict), state, target_func, query_str, field_args_dict)
                result = rs_search.search()

            results[(target, state)] = result

    for (target, state), (inputs, value) in results.items():
        print("Target func: {}, branch: ({}), state {} with inputs {}".format(
            target_func, target, state, inputs))


def run(graphene_schema_path: str, graphql_schema_path: str, strategy: str):
    """[summary]
    Parse python schema file 
    Generate copy of the AST (just in case)
    Find all branches within the tree
    Execute search on the tree with the found targets
    Args:
        :param graphene_schema (str): Path to graphene schema file
        :param graphql_schema_path: Path to graphql schema file
        :param strategy: Search strategy to use
    """
    schema_tree = astor.parse_file(graphene_schema_path)
    query_dict = get_query_dict(graphql_schema_path)

    for func_name, query_field_args_dict in query_dict.items():
        query = query_field_args_dict["query"]
        field_args_dict = query_field_args_dict["field_args_dict"]

        targets = get_targets(copy.deepcopy(schema_tree), func_name)
        do_search(copy.deepcopy(schema_tree), targets, strategy, func_name, query, field_args_dict)

