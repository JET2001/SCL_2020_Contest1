import math
import itertools
import collections
import sys
import bisect ## for bisection algorithms
import operator
import heapq as minheap
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
## =========== DEFINE ANY USER DEFINED CLASSES HERE ==============
class TrieNode:
    def __init__(self, itemName: str):
        self.name = itemName
        self.next = list()
        self.seqno = set()

class Trie:
    def __init__(self):
        self.vertex_list = dict() ## map from name:string to LIST of node:Tries that share the same name
        self.root = TrieNode("-1") ## represent the root as a -1 flag


    def add_item(self, itemName: str, currNode: TrieNode, seqno: int): ## prev is a str, otherwise it defaults to None
        '''Adds item to the trie, typically it will not be a last node nor the first node. So return a reference to the current nextNode in the trie.
        '''
        ## Add sequence number to current node
        print("CurrNode", vars(currNode))
        currNode.seqno.add(seqno)

        for node in currNode.next:
            if itemName in node.name: return node
        ### At this point, node is not present as neighbouring node
        newNode = TrieNode(itemName)
        currNode.next.append(newNode)
        if itemName not in self.vertex_list:
            self.vertex_list[itemName] = list()
        self.vertex_list[itemName].append(newNode)
        return newNode


    def add_query(self, query: list, query_no:int): ##query - list of strings
        ## insert first item
        null_terminator = '$'+ str(query_no) ## just to make sure that it is unique.
        currNode = self.add_item(query[0], self.root, query_no) # no predecessor.
        ## Insert all following items
        for i in range(1,len(query)):
            currNode = self.add_item(query[i], currNode, query_no)

        ## append the null terminating character to the end of each query
        _ = self.add_item(null_terminator, currNode, query_no)
        # print("Added {} to trie".format(query))

    def search_item(self, currNodes: list(), itemToSearch: str):
        '''Returns a list of nodes that are present in the vertex list which map to the string'''
        if len(currNodes) == 1 and currNodes[0] == self.root: ## if its the root, just check if there are any possible value
            return self.vertex_list[itemToSearch] if itemToSearch in self.vertex_list else False

        else:
            ## Check that the currNode has a nextNode that has the search parameter.
            next_nodes = list()
            for currnode in currNodes:
                for next_node in currnode.next:
                    if next_node.name == itemToSearch:
                        next_nodes.append(next_node) ## pack node in list
            ## if code reaches here, node is not present in that node. So no matches with database.
            return False if len(next_nodes) == 0 else next_nodes

    def search_query(self, query: list):
        idx = 0 ## points to the index of the list we would like to search
        currNodes = [self.root]
        while (idx < len(query)):
            currNodes = self.search_item(currNodes, query[idx])
            if currNodes == False: return 0 ## no entry in database
            idx+=1
        ## When we break out of this loop, obtain the possible sequences and return that value
        ## If query has only 1 element
        matches = set()
        ## number of matches will be the sum of the unique sequence numbers between all the satisfiable nodes.
        for node in currNodes:
            for no in node.seqno:
                matches.add(no)

        return len(matches)

#### ========== MAIN IMPLEMENTATION ===========
def question2(item_list: list(), query_list: list()):
    ### Parse input
    output = list()
    search_engine = Trie()
    for idx, item in enumerate(item_list):
        search_engine.add_query(item, idx)
    ## Debug
    print(vars(search_engine))
    for k,v in vars(search_engine)['vertex_list'].items():
        for item in v:
            print(k, vars(item))
    for query in query_list:
        output.append(search_engine.search_query(query))

    return output


### Read first line of input
num_test_cases = int(sys.stdin.readline()) ### template for input with test cases
for i in range(1,num_test_cases+1):
    ### INPUT HERE
    var1, var2 = sys.stdin.readline().split()
    n, q = int(var1), int(var2)
    database = list()
    queries = list()
    ## Process database
    for _ in range(n):
        database.append(sys.stdin.readline().split())
    ## Process queries
    for _ in range(q):
        queries.append(sys.stdin.readline().split())
    output = question2(database, queries)
    print("Case {}:".format(i))
    for _ in output:
        print(_)
# ### PRINT OUTPUT
# output = question2(database, queries)
# for testcase, ans in enumerate(output, start = 1):
#     print("Case {}: {}".format(testcase, ans))
