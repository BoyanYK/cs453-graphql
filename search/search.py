import astor
import copy
from search import avm
from instrumentation.transformer import ResolverInstrumentation
from instrumentation.execution import get_targets

def do_search(schema, targets, args=1, target_func="resolve_char"):
    results = {}
    for target, path in targets.items():
        # * Each target can have a True and a False state
        for state in [True, False]:
            schema_copy = copy.deepcopy(schema)
            instrumentation = ResolverInstrumentation(target, path, target_func)
            instrumented_schema = instrumentation.visit(schema_copy)
            avm_search = avm.AVM(instrumented_schema, path, args, state, target_func)
            result = avm_search.search()

            results[target] = result

    print(results)

def run(schema_path):
    schema_tree = astor.parse_file(schema_path)
    copy_schema_tree = copy.deepcopy(schema_tree)
    targets = get_targets(copy_schema_tree)
    do_search(schema_tree, targets)

