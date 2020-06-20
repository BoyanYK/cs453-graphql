import graphene
import graphql

import subprocess
from os import listdir
from os.path import isfile, join


def generate_queries(sdl_path, depth_limit):
    p = subprocess.Popen(['node', './gql-generator/index.js', '--schemaFilePath', sdl_path, '--destDirPath', './output', '--depthLimit', str(depth_limit)])
    p_status = p.wait()
    queries = [f for f in listdir("./output/queries") if join('./output/queries', f)[-4:]== ".gql"]

    query_dictionary = {}

    for query in queries:
        query_function_name = "resolve_" + query[:-4]
        query_file = "./output/queries/" + query
        with open(query_file, 'r') as file:
            data = file.read()
            query_dictionary[query_function_name] = data
    
    return query_dictionary    

#example usage
query_dict = generate_queries("./../starwars/schema.graphql", 100)

for key in query_dict.keys():
    print("function name : "+ key)
    print("query follows")
    print(query_dict[key])
