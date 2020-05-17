package com.cs453.book.cs453book;

import graphql.ExecutionResult;
import graphql.ExecutionResultImpl;
import graphql.execution.instrumentation.*;
import graphql.execution.instrumentation.parameters.InstrumentationExecutionParameters;
import graphql.execution.instrumentation.parameters.InstrumentationExecutionStrategyParameters;
import graphql.execution.instrumentation.parameters.InstrumentationFieldFetchParameters;
import graphql.schema.DataFetcher;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.logging.Logger;

public class CS453Instrumentation extends SimpleInstrumentation {

    class CustomInstrumentationState implements InstrumentationState {
        private Map<Object, Object> someState = new HashMap<>();

        void recordTiming(Object key, long time) {
            someState.put(key,time);
        }
    }

    @Override
    public InstrumentationState createState() {

        return new CustomInstrumentationState();
    }

    @Override
    public InstrumentationContext<ExecutionResult> beginExecution(InstrumentationExecutionParameters parameters) {
        long startNanos = System.nanoTime();
        return new SimpleInstrumentationContext<ExecutionResult>() {
            @Override
            public void onCompleted(ExecutionResult result, Throwable t) {
                CustomInstrumentationState state = parameters.getInstrumentationState();
                state.recordTiming("time taken(ns)", System.nanoTime() - startNanos);
            }
        };
    }



    @Override
    public DataFetcher<?> instrumentDataFetcher(DataFetcher<?> dataFetcher, InstrumentationFieldFetchParameters parameters) {
        //System.out.println(parameters.getEnvironment());

        return dataFetcher;
    }

    @Override
    public CompletableFuture<ExecutionResult> instrumentExecutionResult(ExecutionResult executionResult, InstrumentationExecutionParameters parameters) {
        CustomInstrumentationState state = parameters.getInstrumentationState();
        return CompletableFuture.completedFuture(new ExecutionResultImpl(executionResult.getData(), executionResult.getErrors(), state.someState));

    }
}
