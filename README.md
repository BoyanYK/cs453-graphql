# cs453-graphql

## Repository for CS453 Automated Software Testing Group Project

The starwars folder is from an example graphene project [link](https://github.com/graphql-python/graphene/tree/master/examples/starwars). It contains the GraphQL Schema in the `schema.py` file and the resolvers for the schema. Tests for the sample API can be seen in the starwars/tests folder. Changes has been made to the structuring of the tests so that there is no model persistence across tests and every test query or mutation can easily be executed against a instrumented schema.

## Requirements
The name of the schema variable in the schema path should be `schema`.

    Python 3.7
    
    pip install -r requirements.txt

###To Run:
    python GenQL.py
Args:
- `-gp, --graphene-schema` default = 'examples/starwars/schema_2.py', Path to a graphene schema definition file.
- `-gql, --graphql-schema` default = 'examples/starwars/schema.graphql', Path to a GraphQL schema definition file.
- `-st, --strategy` default = 'avm_gs', Search strategy to use. args: avm_ips | avm_gs | rs
- `-p, --profiler` default = 1, Number of times to repeat runs.


###Group Members:
>[@BoyanYK](https://github.com/BoyanYK)
>
>[@devturnip](https://github.com/devturnip)
>
>[@iriszero](https://github.com/iriszero)
>
>[@paulkth2](https://github.com/paulkth2)