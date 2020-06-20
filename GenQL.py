import argparse
from search.search import run



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--schema', default='starwars/schema_2.py', 
                        type=str, help='Path to schema definition file')
    args = parser.parse_args()

    schema_path = args.schema
    run(schema_path)





if __name__ == "__main__":
    main()