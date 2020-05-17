package com.cs453.book.cs453book;

import com.google.common.base.Charsets;
import com.google.common.io.Resources;
import graphql.GraphQL;
import graphql.schema.GraphQLSchema;
import graphql.schema.idl.RuntimeWiring;
import graphql.schema.idl.SchemaGenerator;
import graphql.schema.idl.SchemaParser;
import graphql.schema.idl.TypeDefinitionRegistry;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.io.IOException;
import java.net.URL;

import static graphql.schema.idl.TypeRuntimeWiring.newTypeWiring;

@Component

public class BookProvider {

    private GraphQL graphQL;

    @PostConstruct
    public void init() throws IOException {
        URL url = Resources.getResource("schema.graphqls");
        String sdl = Resources.toString(url, Charsets.UTF_8);
        GraphQLSchema graphQLSchema = buildSchema(sdl);
        this.graphQL = GraphQL.newGraphQL(graphQLSchema)
                .instrumentation(new CS453Instrumentation()) //adds instrumentation capabilities
                .build();
    }
    //We use Guava Resources to read the file from our classpath,
    // then create a GraphQLSchema and GraphQL instance.
    // This GraphQL instance is exposed as a Spring Bean
    // via the graphQL() method annotated with @Bean.
    // The GraphQL Java Spring adapter will use that GraphQL instance
    // to make our schema available via HTTP on the default url /graphql.

    @Autowired
    GraphQLDataFetcher graphQLDataFetcher;

    private GraphQLSchema buildSchema(String sdl) {
        TypeDefinitionRegistry typeRegistry = new SchemaParser().parse(sdl);
        RuntimeWiring runtimeWiring = buildWiring();
        SchemaGenerator schemaGenerator = new SchemaGenerator();
        return schemaGenerator.makeExecutableSchema(typeRegistry, runtimeWiring);
    }

    private RuntimeWiring buildWiring() {
        return RuntimeWiring.newRuntimeWiring()
                .type(newTypeWiring("Query")
                        .dataFetcher("bookById", graphQLDataFetcher.getBookByIdDataFetcher()))
                .type(newTypeWiring("Book")
                        .dataFetcher("author", graphQLDataFetcher.getAuthorDataFetcher())
                        .dataFetcher("pageCount", graphQLDataFetcher.getPageCountDataFetcher()))
                .build();

    }

    @Bean
    public GraphQL graphQL() {

        return graphQL;
    }

}
