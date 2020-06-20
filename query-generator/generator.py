import graphene
import graphql

import subprocess
from os import listdir
from os.path import isfile, join
import 

def generate_queries(sdl_path, out_path, depth_limit):
    os_execute = "node ./gql-generator/index.js --schemaFilePath " + sdl_path + " --destDirPath " + out_path + " --depthLimit "+ str(depth_limit)
    subprocess.check_call(['node', './gql-generator/index.js', '--schemaFilePath', sdl_path, '--destDirPath', out_path, '--depthLimit', str(depth_limit)])

    onlyfiles = [f for f in listdir(out_path+"/queries") if isfile(join(out_path, f))]

    print(onlyfiles)
    

generate_queries("./../starwars/schema.graphql", "./output", 100)

