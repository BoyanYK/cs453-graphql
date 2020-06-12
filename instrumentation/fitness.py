import math
from instrumentation.execution import run_test

def get_approach_level(node_path, exec_path):
    """[summary]
    This function iterates through both the expected and execution path and calculates the approach level
    Returns values necessary for fitness function calculation and condition satisfaction
    Args:
        node_path (list): Expected path to a node based on instrumentation
        exec_path (list): Execution trace of nodes after running a test

    Returns:
        tuple: Tuple containing (approach_level, branch/predicate value, branch_distance)
    """
    approach = len(node_path) - 1
    branch_test = None
    branch_distance = 1000
    for executed in exec_path:
        for node in node_path:
            if node.compare(executed):
                current_approach = len(node_path) - list(node_path.keys()).index(node) - 1
                if current_approach < approach or current_approach == 0:
                    approach = current_approach
                    branch_test = executed[1]
                    branch_distance = executed[3]
                    break

    return approach, branch_test, branch_distance

def calculate_fitness(schema, inputs, path, context_trace, query=""):
    """[summary]
    This function is a helper to simplify the execution of a test and fetching the results
    Args:
        schema (schema): Schema object to execute against
        inputs (list): Inputs/arguments to pass to query
        path (list): Expected (correct) path to target
        context_trace (list(tuple)): Actual execution path of function
        query (str, optional): GraphQL Query/Mutation to execute. Defaults to "".

    Returns:
        tuple: Tuple containing (fitness_value, branch/predicate value, approach_level)
    """    
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