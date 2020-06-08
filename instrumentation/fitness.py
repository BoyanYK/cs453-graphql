def get_approach_level(node_path, exec_path):
    approach = len(node_path) - 1
    for node in node_path:
        for executed in exec_path:
            if executed.compare(node):
                current_approach = len(exec_path) - exec_path.index(executed) - 1
                if current_approach < approach or current_approach == 0:
                    approach = current_approach
                    break
    return approach

def calculate_fitness(context_trace):
    # ? context trace should contain the executed trace, alongside booleans for the branches
    # ? execution trace would be a list of tuples as its easiest to handle without needing to insert complex structures as part of instrumentation
    # Unpack context trace - (expr, test_val, lineno, branch_dist)
    pass