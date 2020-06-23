import os, sys

# * Code from https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
# Disable Printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Restore Printing
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stdout = sys.__stderr__

class AnswerFound(Exception):
    pass