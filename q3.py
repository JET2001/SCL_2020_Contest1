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
### O(ns) time
def question3(n: int, s: int, prices: list):
    ### Parse input
    ## create a matrix
    # zeros = [0] * s
    # minCost = [zeros] * (n+1)
    leftMinCost = create_matrix(n+1,s)
    rightMinCost = create_matrix(n+1,s)
    ## corner cases
    if n == 0: return 0
    if n == 1 or n == 2: return min(prices) ## because you can always pick the adjacent index
    ### Assume that it's not possible for n to be equal to 0 (for the sake of our matrix)
    for _ in range(s):
        leftMinCost[0][_] = INT_MAX ## positive infinity
        rightMinCost[0][_] = INT_MAX ## positive infinity
    for i in range(s):
        leftMinCost[1][i] = min(prices[:i+1])
        rightMinCost[1][s-i-1]= min(prices[s-i-1:s])
        print("prices=", prices[s-i-1:s])
        # print(leftMinCost[1][i])
    for i in range(n+1):
        print(leftMinCost[i])
    for i in range(n+1):
        print(rightMinCost[i])
    ## Fill up the leftMinCost array
    for i in range(2, n+1):
        for j in range(s):
            if i > j+1:
                leftMinCost[i][j] = INT_MAX
                continue
            # Consider case where i is odd
            if i % 2 == 1: ## need to buy 1 more cell
                leftMinCost[i][j]= min(leftMinCost[i-1][j-1] + prices[j], leftMinCost[i][j-1])
            else:
                leftMinCost[i][j]= min(leftMinCost[i-1][j], leftMinCost[i-1][j-1], leftMinCost[i][j-1])
        print('i = {}, j= {}'.format(i,j))
        for k in range(n+1):
            print(leftMinCost[k])
    ## Fill up the rightMinCost array - fill this matrix from right to left
    print("==========rightMinCost=========")
    for i in range(2, n+1):
        for j in range(s-1, -1, -1):
            print("i = {}, j = {}".format(i, j))
            if i > s-j:
                rightMinCost[i][j] = INT_MAX
            elif i % 2 == 1:
                rightMinCost[i][j] = min(rightMinCost[i-1][j+1] + prices[j], rightMinCost[i][j+1])
            else:
                rightMinCost[i][j] = min(rightMinCost[i-1][j+1], rightMinCost[i-1][j+1], rightMinCost[i-1][j])

            for k in range(n+1):
                print(rightMinCost[k])

    # for i in range(n+1):
    #     print(leftMinCost[i])

    return min(leftMinCost[n][s-1], rightMinCost[n][0])



### Read first line of input
num_test_cases = int(sys.stdin.readline()) ### template for input with test cases
for i in range(1,num_test_cases+1):
    ### INPUT HERE
    var1, var2 = sys.stdin.readline().split()
    s, n = int(var1), int(var2)
    prices = sys.stdin.readline().split(); prices = [int(x) for x in prices]

    ### PRINT OUTPUT
    output = question3(n, s, prices)
    print("Case {}: {}".format(i, output))


### FAILS ON SORTED ARRAY
