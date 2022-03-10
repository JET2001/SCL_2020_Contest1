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
##### UTILITY FUNCTIONS
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
class PriceItem:
    def __init__(self, row: int, col: int, value: int):
        self.row = row
        self.col = col
        self.value = value
        self.other = None ## initially none, but will be set later, when we discover the max val
        self.include = list() ## if this price item is included in other values
        self.taken = False ## set to True when a token is used to occupy this item.
        self.max_val = INT_MIN ## this is the value that the token acquires after picking the cell.
        self.priority = -self.max_val

    def update_priority(self):
        self.priority = -self.max_val

    def __lt__(self, other):
        return self.priority < other.priority

### Helper Functions
def compute_max(price_matrix, row: int, col: int, max_row: int, max_col: int):
    max_so_far = INT_MIN
    max_idx = (None, None)
    possible_neighbours = []
    if row < max_row:
        possible_neighbours.append((row+1, col))
    if row > 0:
        possible_neighbours.append((row-1, col))
    if col < max_col:
        possible_neighbours.append((row, col+1))
    if col > 0:
        possible_neighbours.append((row, col-1))

    for row_, col_ in possible_neighbours:
        if price_matrix[row_][col_].taken == True: continue
        curr_val = price_matrix[row][col].value + price_matrix[row_][col_].value
        if (curr_val > max_so_far):
            max_so_far = curr_val
            max_idx = (row_,col_)
    return max_so_far, max_idx




#### ========== MAIN IMPLEMENTATION ===========
def question4(matrix, n: int, k: int):
    ### Parse input
    price_matrix = create_matrix(n,k, None)
    ## Iterate through this matrix and place the value of each item inside each index
    for i in range(n): # O(n)
        for j in range(3):
            price_matrix[i][j] = PriceItem(i, j, matrix[i][j])
    ## Debug
    print("PriceMatrix Original")
    for i in range(n):
        for j in range(3):
            print(vars(price_matrix[i][j]))

    ## Traverse the matrix, compute the max sum for each cell of the matrix.
    ## O(n) time
    maxHeap = []
    last_item_idx = -1 #to be used in the heap
    # heapq.heapify(maxHeap) ## actually a minHeap, but our priority is set to the negative.
    for i in range(n):
        for j in range(3):
            price_matrix[i][j].max_val, max_idx = compute_max(price_matrix, i, j, n-1, 2)
            if max_idx == (None, None): continue ## proceed with another index
            ## Since maxidx is not null, that means we still can select this price.
            row_, col_ = max_idx
            ## Found the other cell
            price_matrix[i][j].other = price_matrix[row_][col_]
            price_matrix[row_][col_].include.append(price_matrix[i][j])
            price_matrix[i][j].update_priority()
            maxHeap.append(price_matrix[i][j]) ## push object onto maxHeap.
            last_item_idx += 1
    ## Obtain the max_val in the list
    ## O(n) time
    heapq.heapify(maxHeap)

    print("Initial MaxHeap:")
    for item in list(maxHeap):
        print(vars(item))
    ## O(n*k) time --> O(n^2) time
    max_output = 0
    for token in range(k):
        ## Swap this item with the last item in the heap
        maxPriceItem = maxHeap[0]
        while (maxPriceItem.taken == True):
            _ = heapq.heappop(maxHeap)
            last_item_idx -=1
            maxPriceItem = maxHeap[0]
        ## Have found the maxPriceItem that has not been already selected
        maxHeap[0], maxHeap[last_item_idx] = maxHeap[last_item_idx], maxHeap[0]
        maxPriceItem = maxHeap.pop() ## Remove last item, O(1)

        max_output += maxPriceItem.max_val
        ### Process this max_val
        maxPriceItem.taken = maxPriceItem.other.taken = True # set the value of this maxPriceItem to be True
        for item in [maxPriceItem, maxPriceItem.other]:
            for neighbour in item.include: ## get all cells that also depend on the value of this cell
                if neighbour == maxPriceItem or neighbour == maxPriceItem.other: continue ## may depend on each other
                i, j = neighbour.row , neighbour.col
                price_matrix[i][j].max_val, max_idx = compute_max(price_matrix, i, j, n-1, 2)
                price_matrix[i][j].update_priority() # Change the priorities
                if max_idx == None: continue
                row_, col_ = max_idx
                ## Found the other cell
                price_matrix[i][j].other = price_matrix[row_][col_]
                price_matrix[row_][col_].include.append(price_matrix[i][j])
                price_matrix[i][j].update_priority()

        ## Reprocess the maxHeap
        heapq.heapify(maxHeap) ## O(n) time

        print("==========Token No. {}, current_output: {}==========".format(token+1, max_output))
        print("MaxHeap after token #{}".format(token+1))
        for item in list(maxHeap): print(vars(item))
        print("====================================================")
        last_item_idx -= 1


    return max_output

### Read first line of input
# num_test_cases = int(sys.stdin.readline()) ### template for input with test cases
### INPUT HERE
##### First line of test case
var1, var2 = sys.stdin.readline().split()
n, k = int(var1), int(var2)
matrix = create_matrix(n, 3)
### ANY OTHER INPUT SPECIFICS
## =================================================
for i in range(n):
    var3, var4, var5 = sys.stdin.readline().split()
    matrix[i][0], matrix[i][1], matrix[i][2] = int(var3), int(var4), int(var5)
## =================================================
### PRINT OUTPUT
output = question4(matrix, n, k) ## EDIT PARAMS
print(output)
