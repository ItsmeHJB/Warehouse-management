#Header:
# File:           Base file.py
# Purpose:        To contain all the basic classes for coursework 2 (dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

#Import ibraries

#Define classes
class Item:
    def __init__(self, name, cost, shape, weight):
        self.desc = desc
        self.cost = cost
        self.shape = shape
        self.weight = weight
      
class Shelf:
    def __init__(self, numberOfItems, shape):
        self.numOfItems = numberOfItems
        self.shape = shape
        
class Warehouse:
    def __init__(self, name):
        self.name = name
        
        