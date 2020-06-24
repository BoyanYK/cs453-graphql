import argparse
from search.search import run
import timeit
from search.utils import countFunctionCalls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-gp', '--graphene-schema', default='examples/starwars/schema_2.py',
                        type=str, help='Path to a graphene schema definition file')
    parser.add_argument('-gql', '--graphql-schema', default='examples/starwars/schema.graphql',
                        type=str, help='Path to a GraphQL schema definition file')
    parser.add_argument('-st', '--strategy', default='avm_ips',
                        type=str, help='Search strategy to use. args[avm_ips|avm_gs|rs]')
    parser.add_argument('-p', '--profiler', default=0,
                        type=int, help='number of times to repeat runs. default is 0.')
    args = parser.parse_args()

    profiler = args.__dict__['profiler']

    count = 0
    total_time = 0
    countFunctionCalls.counter = 0
    temp = 0
    if profiler > 0:
        for i in range(0, profiler):
            try:
                print("Run:", i+1)
                start = timeit.default_timer()
                run(args.graphene_schema, args.graphql_schema, args.strategy)
                stop = timeit.default_timer()
                total_time += (stop-start)
                count += 1
            except:
                print("Current run failed")
                count += 1

            print("ITR_Total loops:", countFunctionCalls.counter-temp, "| ITR_Total time taken(secs):",stop-start)
            temp = countFunctionCalls.counter
        print("\nTotal runs taken:", count, "| Total time taken(secs):", total_time, "| Average Time Taken(secs):", total_time/count)
        print("Total loops:", countFunctionCalls.counter, "| Average loops:", countFunctionCalls.counter/count)
    else :
        run(args.graphene_schema, args.graphql_schema, args.strategy)


if __name__ == "__main__":
    main()