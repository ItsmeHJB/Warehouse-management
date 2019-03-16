# File:           ArtPart2.py
# Purpose:        Part 2 of the coursework(dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

# Import libraries
import csv
from pathlib import Path

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

    def add_item(self, art_piece, shelf_number):
        self.shelves[shelf_number].items.append(art_piece)
        self.insurance = self.insurance + art_piece.value


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


# Function to import the start items for a warehouse
def import_items(warehouse, filename):
    with open(filename, mode='r') as csv_file:  # open each file for reading
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:  # loop through csv file
            if line_count == 0:  # Ignore the file headers
                line_count += 1
            else:  # assign id, description, value, shape and weight to item array in warehouse
                row[0] = int(row[0])
                row[2] = int(row[2])
                row[4] = int(row[4])
                for shelf in range(len(warehouse.shelves)):
                    if warehouse.shelves[shelf].shape == row[3]:
                        # print(row)
                        new_item = Item(row[0], row[1], row[2], row[3], row[4])
                        warehouse.shelves[shelf].items.append(new_item)
                        warehouse.insurance = warehouse.insurance + new_item.value


# Function to see if there's space in a warehouse
def check_shelf(art_piece, shelf):
    if (len(shelf.items) < shelf.max_slots) and (art_piece.weight <= shelf.weight):
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
    file = "../" + warehouseList[i].name + 'Shelves.csv'
    cur_path = Path(__file__).parent
    shelf_path = (cur_path / file). resolve()
    import_warehouse_shelf(warehouseList[i], shelf_path)

print("Importing the start items to begin the program\n")
# Import the start items into their warehouses
for i in range(len(warehouseList)):
    file = "../" + warehouseList[i].name + '.csv'
    cur_path = Path(__file__).parent
    item_path = (cur_path / file).resolve()
    import_items(warehouseList[i], item_path)

# BEGIN CODE FOR SPECIFIC TASK ##########################################################
trip_holder = []
total_warehouse_insurance = 0


class Van:
    def __init__(self, items, start, end):
        self.items = items
        self.start_warehouse = start
        self.end_warehouse = end
        self.weight = 2000
        self.max_insurance = 1500000000


def warehouse_name_to_index(name):
    conversion = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3
    }
    return conversion.get(name)


print("Importing the items to be transported by the van")
# Import items to be transported by the van
with open('trips.csv', mode='r') as items_file:
    items_reader = csv.reader(items_file)
    line_count = 0
    for value in items_reader:  # loop through csv file
        if line_count == 0:  # Ignore the file headers
            line_count += 1
        else:  # assign values to the trip holder list
            value[0] = int(value[0])
            value[1] = warehouse_name_to_index(value[1])
            value[2] = warehouse_name_to_index(value[2])
            trip_holder.append([value[0], value[1], value[2 ]])
