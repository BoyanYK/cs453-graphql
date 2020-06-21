import astor
import copy
from .execution import get_targets
from .transformer import ResolverInstrumentation

tree = astor.parse_file("starwars/schema.py")

target_func = "resolve_human"
tree_copy = copy.deepcopy(tree)
targets = get_targets(tree_copy, target_func)

for target, path in targets.items():
    for state in [False, True, False]:
        tree_copy = copy.deepcopy(tree)
        path[target] = state
        instrumentation = ResolverInstrumentation(target, path, target_func)
        modified = instrumentation.visit(tree_copy)
        # print(astor.to_source(modified))