from instrumentation.fitness import calculate_fitness
from math import floor, ceil
import random
import copy
from .utils import AnswerFound

class AVM():
    def __init__(self, tree, path, arg_count, state, func_name="test_me", attempts=10):
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

    def get_f(self, inputs, index, value):
        inputs[index] = value
        if str(inputs) in self.results:
            return self.results[str(inputs)]
        else:
            fitness, branch_state, approach_level = calculate_fitness(self.tree, inputs, self.path, self.func_name)
            if approach_level == 0 and branch_state == self.state:
                self.answer = inputs, (fitness, branch_state, approach_level)
                # * We raise an exception because its the easiest way to exit out of multiple nested loops without adding a lot of boolean flags
                raise AnswerFound
            self.results[str(inputs)] = fitness
            return fitness

    def satisfied_condition(self, inputs):
        return calculate_fitness(self.tree, inputs, self.path, self.func_name)[1] == self.state

    def search(self, inputs=None):
        self.avm(self.avm_gs, inputs)

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
                    return inputs, calculate_fitness(self.tree, inputs, self.path, self.func_name)
                inputs[i] = value
            if self.satisfied_condition(inputs):
                return inputs, calculate_fitness(self.tree, inputs, self.path, self.func_name)
            inputs = None
            self.range *= 10
        return "Unable to find solution", inputs

    def avm_gs(self, inputs, index):
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