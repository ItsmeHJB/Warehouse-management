# Header:
# File:           Base file.py
# Purpose:        To contain all the basic classes for coursework 2 (dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

# Import libraries
import csv

# Declare global variables
MAX_WAREHOUSE_VALUE = 2000000000
MAX_TOTAL_VALUE = 8000000000


# Define classes
# Item class to represent a piece of art
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
        self.shelves = []
        self.insurance = 0
    
    def add_shelf(self, shape, number_of_slots, weight_limit):
        shelf = Shelf(shape, number_of_slots, weight_limit)
        self.shelves.append(shelf)
        
        
# Define functions
# Import the shelves for the 4 warehouses with this from CSV files
def import_warehouse_shelf(warehouse, filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = 0
        for row in csv_reader:  # loop through csv file
            if row_count == 0:  # Ignore the file headers
                row_count += 1
            else:  # assign values to their respective areas from csv
                row[1] = int(row[1])  # converts str to int from csv
                row[2] = int(row[2])
                warehouse.add_shelf(row[0], row[1], row[2])
                
                
# Small dictionary to convert the shape names to letters #################################### DO I NEED THIS?
# def convert(shape):
#    return {
#        'Rectangle': 'R',
#        'Sphere': 'C',
#        'Pyramid': 'P',
#        'Square': 'S',
#    }[shape]


# Small dictionary to convert the letters back to letters

               
# Function to see if there's space in a warehouse
def check_shelf(art_piece, shelf):
    if (len(shelf.items) < shelf.max_slots) and (art_piece.weight <= shelf.weight):
        shelf.items.append(art_piece)
        return True
    else:
        return False


#####################################################
# Main Code #########################################
#####################################################

print("Welcome to the art dealership\n")

print("Initialising empty warehouses\n")
# Initialise warehouses
A = Warehouse('warehouseA')
B = Warehouse('warehouseB')
C = Warehouse('warehouseC')
D = Warehouse('warehouseD')
warehouseList = [A, B, C, D]
total_insurance = 0

print("Adding shelves to their warehouses\n")
# Add the shelves to their warehouses from CSV files
for i in range(len(warehouseList)):
    file = warehouseList[i].name + 'Shelves.csv'
    import_warehouse_shelf(warehouseList[i], file)
    
# BEGIN CODE FOR SPECIFIC TASK #######################
item_holder = []   
total_warehouse_insurance = 0 

print("Importing the items to be stored")
# Import items to be inserted into warehouse A, load them into a list
with open('items.csv', mode='r') as items_file:
    items_reader = csv.reader(items_file)
    line_count = 0
    for value in items_reader:  # loop through csv file
        if line_count == 0:  # Ignore the file headers
            line_count += 1
        else:  # assign values to the item holder list
            value[0] = int(value[0])
            value[2] = int(value[2])
            # value[3] = convert(value[3])
            value[4] = int(value[4])
            item_holder.append(Item(value[0], value[1], value[2], value[3], value[4]))

warehouse_index = 0
while len(item_holder) > 0:
    item = item_holder[0]
    item_added = False
    
    # If the item to be added will be more than the total remaining warehouse value
    if (total_warehouse_insurance + item.value) > MAX_TOTAL_VALUE:
        print("Error: The item you wish to add will push the total insurance of the warehouses over the total "
              "remaining insurance")
        
    elif (warehouseList[warehouse_index].insurance + item.value) <= MAX_WAREHOUSE_VALUE:
        for index in range(len(warehouseList[warehouse_index].shelves)):
            if warehouseList[warehouse_index].shelves[index].shape == item.shape:
                item_added = check_shelf(item, warehouseList[warehouse_index].shelves[index])

    if item_added:
        total_warehouse_insurance = total_warehouse_insurance + item.value
        warehouseList[warehouse_index].insurance = warehouseList[warehouse_index].insurance + item.value
        item_holder.pop(0)
        warehouse_index = 0
    elif warehouse_index < 4:
        warehouse_index += 1
    else:
        print("There is not space for the item with item number: " + item.id + " in any warehouse. \nThis item will be "
                                                                               "discarded")
        item_holder.pop(0)
        warehouse_index = 0

# Print out the warehouse contents to view the results of the add
for i in range(len(warehouseList)):
    print("\n" + warehouseList[i].name + ":")
    for index in range(len(warehouseList[i].shelves)):
        print("\nShelf shape = " + warehouseList[i].shelves[index].shape)
        for item_index in range(len(warehouseList[i].shelves[index].items)):
            print(str(warehouseList[i].shelves[index].items[item_index].id) + ", " + str(warehouseList[i].shelves[index]
                                                                                         .items[item_index].value))
