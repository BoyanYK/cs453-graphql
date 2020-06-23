import numpy as np

from instrumentation.fitness import calculate_fitness
from math import floor, ceil
import random
import copy
from .utils import AnswerFound


class AVM():
    def __init__(self, tree, path, arg_count, state, func_name, query_str, field_args_dict, attempts=10):
        self.results = {}
        self.tree = tree
        self.path = path
        self.arg_count = arg_count
        self.attempts = attempts
        self.state = state
        self.answer = None
        self.range = 10
        self.iterations = 0
        self.func_name = func_name
        self.query_str = query_str
        self.field_args_dict = field_args_dict

    def get_f(self, inputs: list, index: int, value):
        """[summary]
        Function to handle fitness calculation and end condition satisfaction
        Args:
            inputs (list): The list of inputs we want to test
            index (int): The index within the list of inputs that we want to change (because of AVM)
            value ([type]): The value that we want to try out in the list of inputs

        Raises:
            AnswerFound: Exception serving as a quick way to exit execution when an answer has been found

        Returns:
            float: Fitness value
        """
        # * Substitute the index position of the inputs list with the new value we want to try
        inputs[index] = value
        # * If it has already been encountered (within the dict of results), return the value from there
        if str(inputs) in self.results:
            return self.results[str(inputs)]
        else:
            # * Calculate fitness given these arguments and if we have the correct state and approach level, raise an Exception to stop execution
            # * due to correct answer found
            # * Else, add result to caching table and return fitness
            fitness, branch_state, approach_level = calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)
            if approach_level == 0 and branch_state == self.state:
                self.answer = inputs, (fitness, branch_state, approach_level)
                # * We raise an exception because its the easiest way to exit out of multiple nested loops without adding a lot of boolean flags
                raise AnswerFound
            self.results[str(inputs)] = fitness
            return fitness

    def satisfied_condition(self, inputs: list):
        """[summary]
        Verifies if a list of inputs satisfies the targed condition
        Args:
            inputs (list): Inputs to try

        Returns:
            bool: Whether condition has been satisfied or not
        """
        return calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)[1] == self.state

    def search(self, method, inputs=None):
        """[summary]

        Args:
            method (str, optional): Which AVM method to use. Options are 'avm_ips' and 'avm_gs'
            inputs (list, optional): List of pre-generated starting inputs. Used in case of re-using previous successful inputs. Defaults to None.

        Returns:
            tuple: Results found
        """
        if method == "avm_ips":
            return self.avm(self.avm_ips, inputs)
        elif method == "avm_gs":
            return self.avm(self.avm_gs, inputs)

    def avm(self, method, inputs=None):
        # * How many retries with new values
        for j in range(self.attempts):
            # * If no initializing values, create random inputs in range
            if not inputs:
                inputs = [random.randint(-self.range, self.range) for i in range(self.arg_count)]
            # * Attempt changing each input
            for i, value in enumerate(inputs):
                try:
                    value, fitness = method(inputs, i)
                except AnswerFound:
                    return self.answer
                if fitness <= 0.0 and self.satisfied_condition(inputs):
                    return inputs, calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)
                inputs[i] = value
            if self.satisfied_condition(inputs):
                return inputs, calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)
            inputs = None
            # * Increase initialisation range tenfold
            self.range *= 10
        return "Unable to find solution", inputs

    def avm_gs(self, inputs, index):
        # * Just a basic implementation of AVM Geometric Search
        x = inputs[index]
        fitness = self.get_f(inputs, index, x)
        if self.get_f(inputs, index, x - 1) >= fitness and self.get_f(inputs, index, x + 1) >= fitness:
            return x, fitness
        k = -1 if self.get_f(inputs, index, x - 1) < self.get_f(inputs, index, x + 1) else 1
        while self.get_f(inputs, index, x + k) < self.get_f(inputs, index, x):
            if fitness < 0:
                break
            fitness = self.get_f(inputs, index, x + k)
            x = x + k
            k = 2 * k
        l = min(x - k / 2, x + k)
        r = max(x - k / 2, x + k)
        while l < r:
            if self.get_f(inputs, index, floor((l + r) / 2)) < self.get_f(inputs, index, floor((l + r) / 2) + 1):
                r = floor((l + r) / 2)
            else:
                l = floor((l + r) / 2) + 1
        x = l
        return x, fitness

    def avm_ips(self, inputs, index):
        # * Implementation of AVM Iterated Pattern Search
        x = inputs[index]
        fitness = self.get_f(inputs, index, x)
        while fitness > 0:
            if self.get_f(inputs, index, x - 1) >= fitness and self.get_f(inputs, index, x + 1) >= fitness:
                return x, fitness
            k = -1 if self.get_f(inputs, index, x - 1) < self.get_f(inputs, index, x + 1) else 1
            while self.get_f(inputs, index, x + k) < self.get_f(inputs, index, x):
                if fitness < 0:
                    break
                fitness = self.get_f(inputs, index, x + k)
                x = x + k
                k = 2 * k
        return x, fitness
