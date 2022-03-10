import math
import itertools
import collections
import sys
import bisect
import operator
import heapq
import functools
import decimal
import fractions
import random
import queue

## Create a custom class for items
class Item:
    def __init__ (self, itemID: int, stock_type: str, stock: int, quantity: int, parent = None) : ## parent: Item
        self.child = list()
        self.itemID = itemID
        self.stock_type = stock_type
        self.quantity = quantity
        self.parent = None if itemID == 1 else parent

        if (self.parent != None):
            self.parent.child.append(self) # point the parent node to this node.
        ## Calculate stock of the item
        if itemID == 1:
            ## Root
            self.stock = stock
        else:
            self.stock = math.floor(parent.stock / self.quantity) if stock_type == "Dynamic" else stock

class ItemManager:
    def __init__ (self, root: Item):
        self.root = root
        self.items_list = list()
        self.items_list.append(root)

    ## Takes the current node as the root and updates the stock of everything
    ## in its subtree.
    def update_stock(self, currItem: Item):
        q = queue.Queue()
        q.put(currItem)
        while not (q.empty()):
            item = q.get()
            for child in item.child:
                if child.stock_type == "Fixed": continue
                child.stock = math.floor(currItem.stock / child.quantity)
                q.put(child) ## insert child into queue.

    ## Add item to list
    def addNewItem(self, newItem: Item):
        if newItem.stock_type == 'Dynamic':
            pass
        else: ## updates stock if this is fixed.
            ## Updates
            parent_ = newItem.parent
            multiplier = 1
            ## Find the first fixed stock ancestor
            while(parent_.stock_type != "Fixed"):
                multiplier *= parent_.quantity
                parent_ = parent_.parent
            parent_.stock -= multiplier * newItem.quantity * newItem.stock

            ## Do a BFS from this ancestral node to update everything else in its subtree
            self.update_stock(parent_)

        ## Add to item list
        self.items_list.append(newItem)


### Read and parse input
firstline = sys.stdin.readline().split()
n, m = int(firstline[0]), int(firstline[1])
im = ItemManager(Item(1,"Fixed", m, -1))
counter = 2
for i in range(1,n):
    new_item = None
    input = sys.stdin.readline().split()
    if len(input) == 4:
        ## fixed
        _, parent, qty, stock = input
        new_item = Item(i+1, "Fixed", int(stock), int(qty), im.items_list[int(parent)-1]) ## Add an item to item list
    else:
        ## Dynamic
        _, parent, qty = input
        new_item = Item(i+1, "Dynamic", -1, int(qty), im.items_list[int(parent)-1])
    ## Add item and update stock
    im.addNewItem(new_item)

    print("Adding item ", counter)
    for item in im.items_list:
        print(vars(item))

    counter+=1


#### OUTPUT
for _ in im.items_list:
    print(_.stock)
