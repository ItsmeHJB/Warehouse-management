# File:           ArtPart2A.py
# Purpose:        Part 2A of the coursework(dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

# Import libraries
import csv
from pathlib import Path
import operator

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

    def remove_item(self, art_piece, shelf_number):
        self.shelves[shelf_number].items.remove(art_piece)
        self.insurance = self.insurance - art_piece.value


class Van:
    max_weight = 2000
    max_insurance = 1500000000

    def __init__(self, art_id, start, end):
        self.items = [art_id]
        self.start_warehouse = start
        self.end_warehouse = end

    def add_item(self, art_id):
        self.items.append(art_id)


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
        line_number = 0
        for row in csv_reader:  # loop through csv file
            if line_number == 0:  # Ignore the file headers
                line_number += 1
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


# Dict function to return the warehouse index from it's name
def warehouse_name_to_index(name):
    conversion = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3
    }
    return conversion.get(name)


# Sort the trips with regards to their start and end position. A first, descending to D.
def sort_trips(trips):
    trips.sort(key=operator.itemgetter(1, 2))


# Check if the trip will be valid if we move this item
def check_trip(trip):
    valid_add = False

    art = Item
    # Find the item in the first warehouse
    start_warehouse = trip[1]
    # For all the shelves in the warehouse
    for shelves in range(len(warehouseList[start_warehouse].shelves)):
        # Look through each item to find the right one
        for items in range(len(warehouseList[start_warehouse].shelves[shelves].items)):
            # If the item number matches, we've found our item
            if warehouseList[start_warehouse].shelves[shelves].items[items].id == trip[0]:
                art = warehouseList[start_warehouse].shelves[shelves].items[items]
                start_shelf_index = shelves
                break

    # Check if the item can be moved to the warehouse in a valid fashion
    end_warehouse = trip[2]

    # Check the insurance is enough to cover the item
    if warehouseList[end_warehouse].insurance + art.value <= MAX_WAREHOUSE_VALUE:
        # Find index of shelf we are adding to
        end_shelf_index = find_shelf_index(warehouseList[end_warehouse].shelves, art.shape)
        # Check shelf_index is set, if it isn't then there isn't a valid shelf
        if not end_shelf_index == -1:
            # Check if there is space on the shelf
            valid_add = check_shelf(art, warehouseList[end_warehouse].shelves[end_shelf_index])
            # If it's a valid move, move the item to the warehouse
            if valid_add:
                warehouseList[start_warehouse].remove_item(art, start_shelf_index)
                warehouseList[end_warehouse].add_item(art, end_shelf_index)

    return valid_add


# Function to find the index of a shelf in a warehouse
def find_shelf_index(warehouse_shelves, shape):
    for index in range(len(warehouse_shelves)):
        if warehouse_shelves[index].shape == shape:
            return index


def warehouse_index_to_name(index):
    conversion = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D'
    }
    return conversion.get(index)


# Finds the item in the warehouse and returns it
def find_item(warehouse_index, id_num):
    # For all the shelves in the warehouse
    for shelves in range(len(warehouseList[warehouse_index].shelves)):
        # Look through each item to find the right one
        for items in range(len(warehouseList[warehouse_index].shelves[shelves].items)):
            # If the item number matches, we've found our item
            if warehouseList[warehouse_index].shelves[shelves].items[items].id == id_num:
                return warehouseList[warehouse_index].shelves[shelves].items[items]


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
            value[1] = warehouse_name_to_index(value[1])  # Convert the name to index of each warehouse
            value[2] = warehouse_name_to_index(value[2])
            trip_holder.append([value[0], value[1], value[2]])

# Sort the trips
sort_trips(trip_holder)

# Set the trip counter to 0
number_of_trips = 0
van_insurance = 0
van_weight = 0

# While there are trips to be made
while trip_holder:
    valid = False
    trip_index = -1
    van_weight = 0
    item = Item

    # Look at trips in trip_holder, find first valid item which can be moved
    for i in range(len(trip_holder)):
        # Find the item in the warehouse
        item = find_item(trip_holder[i][1], trip_holder[i][0])

        # Check if it will fit in the Van's constraints
        if van_weight + item.weight <= Van.max_weight:
            # Check if the move is valid
            valid = check_trip(trip_holder[i])
            if valid:  # If it is a valid move to put it in the warehouse
                trip_index = i
                van_weight = van_weight + item.weight
                break

    # Check if we have a valid item to move (trip_index would have been set)
    if not trip_index == -1:
        # Load initial item into van
        van = Van(trip_holder[trip_index][0], trip_holder[trip_index][1], trip_holder[trip_index][2])
        # Pop the item from the trip_holder
        trip_holder.pop(trip_index)
    else:
        # If there are no more moves we can do
        print("\nThere are no more valid trips which can be made")
        break

    # See if there are other items with the same trip
    i = 0
    while i < len(trip_holder):
        # If the start and end warehouses are the same
        if (van.start_warehouse == trip_holder[i][1]) and (van.end_warehouse == trip_holder[i][2]):
            # Find the item we need
            item = find_item(van.start_warehouse, trip_holder[i][0])
            # Check if it fits in the van
            if van_weight + item.weight <= Van.max_weight:
                # Check if the end warehouse can hold the item
                if check_trip(trip_holder[i]):
                    van.add_item(trip_holder[i][0])
                    van_weight = van_weight + item.weight
                    trip_holder.pop(i)
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1

    number_of_trips += 1

    print("\nOn trip number: " + str(number_of_trips) + ". The van travelled from " +
          warehouse_index_to_name(van.start_warehouse) + " to " + warehouse_index_to_name(van.end_warehouse))
    print("These items were moved: ")
    for i in range(len(van.items)):
        print("Item number: " + str(van.items[i]))

print("Total runs: " + str(number_of_trips))
if len(trip_holder) > 0:
    print("Unfortunately, not all the items could be moved. They are listed below: ")
    for i in range(len(trip_holder)):
        print("Item number: " + str(trip_holder[i][0]))
