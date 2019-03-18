# File:           ArtPart4.py
# Purpose:        Part 3 of the coursework (dadsa)
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

    def remove_item(self, art_piece):
        # Find the shelf we need
        for index in range(len(self.shelves)):
            if art_piece.shape == self.shelves[index].shape:
                shelf_number = index
                break
        # Remove item and reduce warehouse insurance
        self.shelves[shelf_number].items.remove(art_piece)
        self.insurance = self.insurance - art_piece.value


class Van:
    max_weight = 2000
    max_insurance = 1500000000
    insurance = 0
    weight = 0
    shelf = None
    start_one = None
    stop_one = None
    start_two = None
    stop_two = None

    def initial_run(self, art, start_warehouse, stop_warehouse):
        self.shelf = VanShelf(art.shape, art.id)
        self.start_one = start_warehouse
        self.stop_one = stop_warehouse
        self.insurance = art.value
        self.weight = art.weight

    def second_drop(self, art, start_warehouse, stop_warehouse):
        self.shelf.add_item(art.id)
        self.start_two = start_warehouse
        self.stop_two = stop_warehouse
        self.insurance += art.value
        self.weight += art.weight

    def add_item(self, art):
        self.shelf.add_item(art.id)
        self.insurance += art.value
        self.weight += art.weight

    def reset_trips(self):
        self.shelf.items.clear()
        self.shelf.shape = None
        self.insurance = 0
        self.weight = 0


class VanShelf:
    items = []

    def __init__(self, shape, item_id):
        self.shape = shape
        self.items.append(item_id)

    def add_item(self, item_id):
        self.items.append(item_id)


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
        row_count = 0
        for row in csv_reader:  # loop through csv file
            if row_count == 0:  # Ignore the file headers
                row_count += 1
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


# Reverse dict for printing at the end
def warehouse_index_to_name(index):
    conversion = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D'
    }
    return conversion.get(index)


# Sort the trips with regards to their start and end position. A first, descending to D.
def sort_trips(trips):
    trips.sort(key=operator.itemgetter(1, 2))


# Finds the item in the warehouse and returns it
def find_item(id_num):
    # For all the warehouses we have
    for warehouse_index in range(len(warehouseList)):
        # For all the shelves in the warehouse
        for shelves in range(len(warehouseList[warehouse_index].shelves)):
            # Look through each item to find the right one
            for items in range(len(warehouseList[warehouse_index].shelves[shelves].items)):
                # If the item number matches, we've found our item
                if warehouseList[warehouse_index].shelves[shelves].items[items].id == id_num:
                    return warehouseList[warehouse_index].shelves[shelves].items[items]


# Check if the trip will be valid if we move this item
def check_trip(art, destination, start):
    valid_add = False
    shelf_index = None

    # Check if dest has the insurance available to cover the move
    if warehouseList[destination].insurance + art.value + van.insurance <= MAX_WAREHOUSE_VALUE:
        # Find the index of shelf we are adding to
        shelf_index = find_shelf_index(warehouseList[destination].shelves, art.shape)
        # Check the shelf is set (will be -1 if not)
        if shelf_index is not None:
            valid_add = check_shelf(art, warehouseList[destination].shelves[shelf_index])
            if valid_add:
                warehouseList[start].remove_item(art)
                warehouseList[destination].add_item(art, shelf_index)

    return valid_add


# Function to find the index of a shelf in a warehouse
def find_shelf_index(warehouse_shelves, shape):
    for index in range(len(warehouse_shelves)):
        if warehouse_shelves[index].shape == shape:
            return index


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

# BEGIN CODE FOR SPECIFIC TASK #######################
item_holder = []

print("Importing the items to be transported by the van")
# Import items to be transported by the van
with open('Part4Trips.csv', mode='r') as items_file:
    items_reader = csv.reader(items_file)
    line_count = 0
    for value in items_reader:  # loop through csv file
        if line_count == 0:  # Ignore the file headers
            line_count += 1
        else:  # assign values to the trip holder list
            value[0] = int(value[0])
            value[1] = warehouse_name_to_index(value[1])  # Convert the name to index of each warehouse
            value[2] = warehouse_name_to_index(value[2])
            item_holder.append([value[0], value[1], value[2]])

# Sort the trips so that similar trips are grouped together
sort_trips(item_holder)

# Set the number of trips to 0 at start
number_of_trips = 0
# While we still have potential trips to do
while item_holder:
    # Initialise van and other things
    van = Van()
    trip_index = -1

    # Look at list of item, find first valid item which can be moved
    for i in range(len(item_holder)):
        # Find the item in the warehouse
        item = find_item(item_holder[i][0])
        # Check if item can fit in the van
        if (van.insurance + item.value <= van.max_insurance) and (van.weight + item.weight <= van.max_weight):
            # Check if the move is valid
            if check_trip(item, item_holder[i][2], item_holder[i][1]):
                # If the move is valid, we put it in the van
                trip_index = i
                van.initial_run(item, item_holder[i][1], item_holder[i][2])
                break  # We only want one item to start it, so break if found

    # Check if we have a valid item to move (trip_index is set)
    if not trip_index == -1:
        # Pop it off the item_holder array
        item_holder.pop(trip_index)
    else:
        # If there are no more possible moves
        print("\nThere are no more valid trips which can be made")
        break

    # See if there are other items which are travelling the same trip, and have identical start & dest
    i = 0
    while i < len(item_holder):
        # If the start and end warehouse are identical
        if (van.start_one == item_holder[i][1]) and (van.stop_one == item_holder[i][2]):
            # Find item we need from the warehouse
            item = find_item(item_holder[i][0])
            # Check if it fits in the van
            if (van.insurance + item.value <= van.max_insurance) and (van.weight + item.weight <= van.max_weight):
                # Check the end warehouse can hold it
                if check_trip(item, van.stop_one, van.start_one):
                    # If move is valid as well, add it to the van
                    van.add_item(item)  # Add to van
                    item_holder.pop(i)
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1

    # Next, check if there are other items which can be moved
    i = 0
    while i < len(item_holder):
        # Check if item has the same start, but different end, so it continues onwards after the first drop OR starts at
        #  first stop, so it drops all and continues to second place OR finishes at the same place so it could be picked
        #  up on route to the final destination
        if van.start_one == item_holder[i][1] or van.stop_one == item_holder[i][1] or van.stop_one == item_holder[i][2]:
            # Find the item we need
            item = find_item(item_holder[i][0])
            # Check if it fits in the van
            if (van.insurance + item.value <= van.max_insurance) and (van.weight + item.weight <= van.max_weight):
                # Check the end warehouse can hold it
                if check_trip(item, item_holder[i][2], item_holder[i][1]):
                    # If this move is valid, add it to the van for transport
                    van.second_drop(item, item_holder[i][1], item_holder[i][2])
                    item_holder.pop(i)
                    break  # We can only do 2 runs, so we break from while loop after finding run 2
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1

    if van.start_two is not None:  # If we are doing a second run
        # Find other trips with the same pattern as trip two OR start_one to stop_two
        i = 0
        while i < len(item_holder):
            # If the start and end warehouse are identical
            if ((van.start_two == item_holder[i][1]) and (van.stop_two == item_holder[i][2])) or (
                    (van.start_one == item_holder[i][1]) and (van.stop_two == item_holder[i][2])):
                # Find item we need from the warehouse
                item = find_item(item_holder[i][0])
                # Check if it fits in the van
                if (van.insurance + item.value <= van.max_insurance) and (van.weight + item.weight <= van.max_weight):
                    # Check the end warehouse can hold it
                    if check_trip(item, van.stop_two, van.start_two):
                        # If move is valid as well, add it to the van transport
                        van.add_item(item)  # Add to van
                        item_holder.pop(i)
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1

    number_of_trips += 1

    trip_string = ("\nOn trip number: " + str(number_of_trips) + ". The van started at " + warehouse_index_to_name(
        van.start_one))
    if van.start_two is not None:
        if van.stop_one == van.start_two:
            trip_string += (" then dropped everything at " + warehouse_index_to_name(van.stop_one) + " followed by" +
                            " finishing at " + warehouse_index_to_name(van.stop_two) + " after picking up more items")
        elif van.stop_one < van.stop_two:
            trip_string += (" then stopped at " + warehouse_index_to_name(van.stop_one) + " to drop some items, "
                            "followed by finishing at " + warehouse_index_to_name(van.stop_two))
        else:
            trip_string += (" then stopped at " + warehouse_index_to_name(van.start_two) + " to pickup more, followed "
                            "by finishing at " + warehouse_index_to_name(van.stop_two))
    else:
        trip_string += (" and finished at " + warehouse_index_to_name(van.stop_one))

    print(trip_string)
    print("These items were moved: ")
    for i in range(len(van.shelf.items)):
        print("Item number: " + str(van.shelf.items[i]))

    van.reset_trips()

print("Total runs: " + str(number_of_trips))
if len(item_holder) > 0:
    print("Unfortunately, not all the items could be moved. They are listed below: ")
    for i in range(len(item_holder)):
        print("Item number: " + str(item_holder[i][0]))
