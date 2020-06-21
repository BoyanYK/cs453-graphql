import argparse
from search.search import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--schema', default='examples/starwars/schema_2.py',
                        type=str, help='Path to schema definition file')
    parser.add_argument('-st', '--strategy', default='avm_ips',
                        type=str, help='Search strategy to use. args[avm_ips|avm_gs|rs]')
    args = parser.parse_args()

    schema_path = args.schema
    strategy = args.strategy
    run(schema_path, strategy)


if __name__ == "__main__":
    main()