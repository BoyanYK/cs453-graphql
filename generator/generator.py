import graphene
import graphql

import subprocess
from os import listdir
from os.path import isfile, join

"""
Runs JS gql-generator library on shell so npm dependencies must be installed.

<Input>
sdl_path : path of sdl file, relative to the current directory where function is called
depth_limit : depth limit suggested by JS library. Shouldn't matter much with starwars(>=2) schema.

<Output>
Dictionary of key(func name) value(query) pair.

<Note>
There are some troubles with output directories when the function is called from other directories.
If this happens, we should either modify the execution directory with os module,
or modify the function to pass relative output path. 
"""
def generate_queries(sdl_path, depth_limit):
    """
    Execute the JS library and save the files.
    Wait until the commandline job finishes, and read the query files in query folder
    """
    p = subprocess.Popen(['node', './gql-generator/index.js', '--schemaFilePath', sdl_path, '--destDirPath', './output', '--depthLimit', str(depth_limit)])
    p_status = p.wait()
    queries = [f for f in listdir("./output/queries") if join('./output/queries', f)[-4:]== ".gql"]

    query_dictionary = {}

    #Generates dictionary
    for query in queries:
        query_function_name = "resolve_" + query[:-4]
        query_file = "./output/queries/" + query
        with open(query_file, 'r') as file:
            data = file.read()
            query_dictionary[query_function_name] = data
    
    return query_dictionary    

#example usage
query_dict = generate_queries("./../starwars/schema.graphql", 100)

#Printing generated example output.
for key in query_dict.keys():
    print("function name : "+ key)
    print("query follows")
    print(query_dict[key])
