import random
from search.avm import AVM
from instrumentation.fitness import calculate_fitness

import numpy as np

from search.utils import AnswerFound


class RS():
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

    def search(self, method="rs", inputs=None):
        """[summary]

        Args:
            method (str, optional): Which AVM method to use. Options are 'avm_ips' and 'avm_gs'
            inputs (list, optional): List of pre-generated starting inputs. Used in case of re-using previous successful inputs. Defaults to None.

        Returns:
            tuple: Results found
        """
        if method == "rs":
            return self.random(self.random_s, inputs)

    def random(self, method, inputs=None):
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
                if fitness <= 0.0 and AVM.satisfied_condition(self, inputs):
                    return inputs, calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)
                inputs[i] = value
            if AVM.satisfied_condition(self, inputs):
                return inputs, calculate_fitness(self.tree, inputs, self.path, self.query_str, self.field_args_dict)
            inputs = None
            # * Increase initialisation range tenfold
            self.range *= 10
        return "Unable to find solution", inputs

    def random_s(self, inputs, index):
        # using abs here is cheating...
        # since we know the range will always be positive
        x = abs(inputs[index])
        print("INPUTS x: ", x)  # TONY
        fitness = AVM.get_f(self, inputs, index, x)

        if AVM.get_f(self, inputs, index, x - 1) >= fitness and AVM.get_f(self, inputs, index, x + 1) >= fitness:
            return x, fitness
        k = -1 if AVM.get_f(self, inputs, index, x - 1) < AVM.get_f(self, inputs, index, x + 1) else 1

        # minimise fitness to 0
        while AVM.get_f(self, inputs, index, x + k) < AVM.get_f(self, inputs, index, x):
            if fitness < 0:
                break

            # if input is not negative, sample new y from range(0,input)
            if x > 0:
                y = np.random.randint(0, x)
            # elif input is negative, sample new y from range(-input,input)
            elif x < 0:
                y = np.random.randint(x, abs(x))
            # elif input is 0, add 10 and sample new y from range(0, 10)
            elif x == 0:
                x = x + 10
                y = np.random.randint(0, x)

            # check fitness with y, sampled from x
            fitness_y = AVM.get_f(self, inputs, index, y)

            # if fitness of y is lesser than fitness of x
            if fitness_y < fitness:
                # BUT if fitness of y is > 1,
                # we want to escape by giving x a larger value
                if fitness_y > 1:
                    x = abs(x) * 10
                # else we make x = y, at this point fitness value should be close
                # to 0 based on observations
                else:
                    x = y

            else:
                # if fitness of y is greater, give x with new value
                # for resampling
                x = abs(x) * 10

        return x, fitness
