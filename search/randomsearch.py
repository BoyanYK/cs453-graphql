import random
from instrumentation.fitness import calculate_fitness

import numpy as np


class RS():
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


    def random(self, inputs=None):
        #for random,
        for j in range(self.attempts):
            # * If no initializing values, create random inputs in range
            # from initial random
            # sample new position y from uniform sampling of x
            # x = y ifff point is improving
            # do i maintain list of tried numbers
            # or since we know x ! <= 0, theres no need since
            # x is np.randint(low)...
            # what about repeating numbers?
            # in essence when an event is random
            # it is possible that the same event may happen again...
            # so repeating numbers???????
            if not inputs:
                inputs = [random.randint(-self.range, self.range) for i in range(self.arg_count)]

            print("INPUTS:", inputs)


print(np.random.randint(1, 6, 5))


