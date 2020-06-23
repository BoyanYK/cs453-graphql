import argparse
from search.search import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-gp', '--graphene-schema', default='examples/starwars/schema_2.py',
                        type=str, help='Path to a graphene schema definition file')
    parser.add_argument('-gql', '--graphql-schema', default='examples/starwars/schema.graphql',
                        type=str, help='Path to a GraphQL schema definition file')
    parser.add_argument('-st', '--strategy', default='avm_ips',
                        type=str, help='Search strategy to use. args[avm_ips|avm_gs|rs]')
    args = parser.parse_args()

    run(args.graphene_schema, args.graphql_schema, args.strategy)


if __name__ == "__main__":
    main()