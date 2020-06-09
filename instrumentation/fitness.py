import math
from instrumentation.execution import run_test

def get_approach_level(node_path, exec_path):
    approach = len(node_path) - 1
    branch_test = None
    branch_distance = 1000
    for executed in exec_path:
        for node in node_path:
            if node.compare(executed):
                current_approach = len(node_path) - exec_path.index(node_path) - 1
                if current_approach < approach or current_approach == 0:
                    approach = current_approach
                    branch_test = executed[1]
                    branch_distance = executed[3]
                    break
    return approach, branch_test, branch_distance

def calculate_fitness(schema, inputs, path, context_trace):
    # ? context trace should contain the executed trace, alongside booleans for the branches
    # ? execution trace would be a list of tuples as its easiest to handle without needing to insert complex structures as part of instrumentation
    # Unpack context trace - (expr, test_val, lineno, branch_dist)
    query = """
        query FetchSomeIDQuery($someId: String!) {
            char(id: $someId) {
                name
            }
        }
    """
    context_trace = run_test(schema, query, inputs)
    approach, branch_test, branch_distance = get_approach_level(path, context_trace)
    fitness = approach + (1 - math.pow(1.0001, -branch_distance))
    return fitness, branch_test, approach