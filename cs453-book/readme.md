# Notes

Java example taken from [here](https://www.graphql-java.com/tutorials/getting-started-with-spring-boot/) .

Currently added custom instrumention that returns query execution time in result.


# How to use

Deploy springboot application
Endpoint will be hosted on [http://localhost:8080/graphql]()
Use [GraphQL Playground (mac)](https://github.com/prisma-labs/graphql-playground) or other equivalent to play with endpoint.


# Goals

Figure out fitness function that takes into account a combination of:
1. GraphQL types hit by input query (types/mutations/queries)

2. Branch coverage
    
    - Caveat: Most GraphQL applications are simple CRUD application that may not necessarily have branches...

3. Based on a GraphQL Schema as input, generate automatic queries for said schema.

4. More automatic test case generation ?
    
   