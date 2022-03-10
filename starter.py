import math
import itertools
import collections
import sys
import bisect ## for bisection algorithms
import operator
import heapq
import functools
import decimal
import fractions
import random
import queue
import typing
### Declare any constants
POS_INF = float('inf')
NEG_INF = float('-inf')
INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize

### Declare any type aliases here
Queue = queue.Queue
Stack = queue.LifoQueue

#### UTILITY FUNCTIONS
### Creating a Matrix in Python
def create_matrix(rows, cols, default_val = 0):
    """
    Creates a matrix filled with default_val
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have

        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(default_val)

    return M
## =========== DEFINE ANY USER DEFINED CLASSES HERE ===============










#### ========== MAIN IMPLEMENTATION ===========
def question1(PARAMS):
    ### Parse input
    pass



### Read first line of input
num_test_cases = int(sys.stdin.readline()) ### template for input with test cases
for i in range(1,num_test_cases+1):
    ### INPUT HERE
    ##### First line of test case
    var1 , var2  = sys.stdin.readline.split()
    a, b, ... = int(var1), int(var2)
    ### ANY OTHER INPUT SPECIFICS
    ## =================================================


    ## =================================================
    ### PRINT OUTPUT
    output = question1(PARAMS) ## EDIT PARAMS
    print("Case {}: {}".format(i, output))
