# Header:
# File:           Base file.py
# Purpose:        To contain all the basic classes for coursework 2 (dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

# Import ibraries
import csv

# Declare global variables
MAX_WAREHOUSE_VALUE = 2000000000
MAX_VALUE = 8000000000

# Define classes
# Item class to reperesent a piece of art
class Item:
    def __init__(self, id_num, description, cost, shape, weight):
        self.id = id_num
        self.desc = description
        self.value = cost
        self.shape = shape
        self.weight = weight
      
# Shelf class to represent where items are stored within a warehouse
class Shelf:
    def __init__(self, shape, number_of_slots, weight_limit):
        self.shape = shape
        self.max_slots = number_of_slots
        self.weight = weight_limit
        self.items = []
  
# Warehouse class to represent the warehouses to hold the items      
class Warehouse:
    def __init__(self, name):
        self.name = name
        self.shelfs = []
        self.insurance = 0
    
    def add_shelf(self, shape, number_of_slots, weight_limit):
        shelf = Shelf(shape, number_of_slots, weight_limit)
        self.shelfs.append(shelf)
        
        
# Define functions
# Import the shelfs for the 4 warehouses with this from CSV files
def import_warehouse_shelf(warehouse, filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:  # loop through csv file
            if line_count == 0:  # Ignore the file headers
                line_count += 1
            else: # assign values to their respective areas from csv
                row[1] = int(row[1]) # converts str to int from csv
                row[2] = int(row[2])
                warehouse.add_shelf(row[0], row[1], row[2])
                
#####################################################
# Main Code #########################################
#####################################################

print("Welcome to the art dealership")

# Initialise warehouses
A = Warehouse('warehouseA')
B = Warehouse('warehouseB')
C = Warehouse('warehouseC')
D = Warehouse('warehouseD')
warehouseList = [A, B, C, D]
total_insurance = 0

# Add the shelfs to their warehouses from CSV files
for i in range(len(warehouseList)):
    file = warehouseList[i].name + 'Shelfs.csv'
    import_warehouse_shelf(warehouseList[i], file)
    
# BEGIN CODE FOR SPECIFIC TASK #######################


        