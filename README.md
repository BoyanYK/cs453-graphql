# cs453-graphql

## Repository for CS453 Automated Software Testing Group Project

The starwars folder is from an example graphene project [link](https://github.com/graphql-python/graphene/tree/master/examples/starwars). It contains the GraphQL Schema in the `schema.py` file and the resolvers for the schema. Tests for the sample API can be seen in the starwars/tests folder. Changes has been made to the structuring of the tests so that there is no model persistence across tests and every test query or mutation can easily be executed against a instrumented schema.
