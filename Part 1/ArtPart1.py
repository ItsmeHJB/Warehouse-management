# File:           ArtPart1.py
# Purpose:        To demonstrate the working code for problem Part 1 (dadsa)
# Author:         Harrison Bennion
# Student Number: 17012546

# PSEUDO CODE for Part 1
# Initialise 4 empty warehouses
# Place these in a list for easy iteration
# Add the shelves to their warehouses from the base files
# Import and add the start items to their warehouses
#
# Import the task specific items from Items.csv
# Load these into a queue based list
#
# While there are still items to add to the warehouse:
#   Get the first item from item queue
#   If item will push total of all warehouses over insurance limit
#       yes -> print error and discard item as it cannot go anywhere
#
#   Check if the item fits in warehouse A
#   If warehouse A has enough insurance to cover the new add:
#       Loop through the shelves in A:
#           If the item shape matches the shelf shape:
#               Check there is space on the shelf for this new item (weight and max slots)
#               If item can be added to shelf:#
#                   Set add flag and set warehouse storage to point to warehouse A
#
#   If add flag is not set: (could not add to A)
#       Clear fitness list of all values
#       Loop through the other 3 warehouses:
#           If there is enough insurance to cover it:
#               Loop through the shelves in the warehouse:
#                   If the shelf shape is the same as the new item:
#                       If there is space on the shelf for this new item:
#                           Find the fit value of adding this item to this warehouse
#                           Append this to a fitness list
#                       else:
#                           break from shelf loop
#
#       If the fitness list has any items in:
#           Set best fit to a large number
#           Loop through fitness list:
#               Find best item from the list -> set best fit to this value
#               Set warehouse storage to point at this warehouse we found to be best
#
#   If we have found a space for the item:
#       Find the shelf in the warehouse to add to
#       Add the item to the warehouse shelf and update warehouse and total insurance
#       Pop this item from the item queue
#   else: (there is no where to put it)
#       Print an error message
#       Pop this item from the queue

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


def check_shelf_fit(art_piece, shelf):
    return shelf.weight - art_piece.weight


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

# BEGIN CODE FOR SPECIFIC TASK #######################
item_holder = []   
total_warehouse_insurance = 0
warehouse_fit = []

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
            value[4] = int(value[4])
            item_holder.append(Item(value[0], value[1], value[2], value[3], value[4]))

# While we still have items to add to the warehouses
while len(item_holder) > 0:
    item = item_holder[0]
    item_to_be_added = False
    
    # If the item to be added will be more than the total remaining warehouse value
    if (total_warehouse_insurance + item.value) > MAX_TOTAL_VALUE:
        print("Error: The item you wish to add will push the total insurance of the warehouses over the total "
              "remaining insurance")

    # check warehouse A on our first run through
    elif (warehouseList[0].insurance + item.value) <= MAX_WAREHOUSE_VALUE:
        # Loop through available shelves
        for index in range(len(warehouseList[0].shelves)):
            # If there is shelf with the right shape
            if warehouseList[0].shelves[index].shape == item.shape:
                # Check if the shelf has space and the right weight for item
                item_to_be_added = check_shelf(item, warehouseList[0].shelves[index])
                if item_to_be_added:  # Successful add possible
                    # Store that the item is going into warehouse A later
                    store_in_warehouse_index = 0
                break

    # If the item cannot be added to warehouse A
    if not item_to_be_added:
        # Reset the warehouse_fit list
        warehouse_fit.clear()
        # Loop through the rest of the warehouses for space in each
        for warehouse_index in range(1, len(warehouseList)):
            # If there is enough warehouse insurance in the current warehouse
            if (warehouseList[warehouse_index].insurance + item.value) <= MAX_WAREHOUSE_VALUE:
                # Loop through available shelves
                for shelf_index in range(len(warehouseList[warehouse_index].shelves)):
                    # If there is shelf with the right shape
                    if warehouseList[warehouse_index].shelves[shelf_index].shape == item.shape:
                        # Check if the shelf has space and the right weight for item
                        if check_shelf(item, warehouseList[warehouse_index].shelves[shelf_index]):
                            # If the item is 100% valid etc, we now find the fit of each warehouse
                            warehouse_fit.append([check_shelf_fit(item, warehouseList[warehouse_index].shelves[
                                shelf_index]), warehouse_index])
                        # If we have found the right shelf in the warehouse -> stop looking at them all
                        else:
                            break

        # After all that, we see if any warehouses can fit, and decided which is best fit
        if len(warehouse_fit) > 0:
            # Set best fit to something big
            best_fit = 999999999
            # Search for best fit (smallest value)
            for fit_index in range(len(warehouse_fit)):
                if warehouse_fit[fit_index][0] < best_fit:
                    best_fit = warehouse_fit[fit_index][0]
                    store_in_warehouse_index = warehouse_fit[fit_index][1]
                    item_to_be_added = True

    # If we have a found a fit for the item somewhere in the code
    if item_to_be_added:
        # Find the index of the shelf it's being added to
        for shelf_index in range(len(warehouseList[store_in_warehouse_index].shelves)):
            if warehouseList[store_in_warehouse_index].shelves[shelf_index].shape == item.shape:
                shelf_to_add_to = shelf_index
                break

        # Add the item to the found warehouse and update total insurance
        warehouseList[store_in_warehouse_index].add_item(item, shelf_to_add_to)
        total_warehouse_insurance = total_warehouse_insurance + item.value

        # Pop item from item_holder list
        item_holder.pop(0)

    # If we cannot add this anywhere
    else:
        print("There isn't space for the item with item number: " + str(item.id) + " in any warehouse. \nThis item "
                                                                                   "will be discarded")
        # Remove it from the queue
        item_holder.pop(0)

# Print out the warehouse contents to view the results of the add
for i in range(len(warehouseList)):
    print("\n" + warehouseList[i].name + ":")
    for index in range(len(warehouseList[i].shelves)):
        print("\nShelf shape = " + warehouseList[i].shelves[index].shape)
        for item_index in range(len(warehouseList[i].shelves[index].items)):
            print(str(warehouseList[i].shelves[index].items[item_index].id) + ", " + str(warehouseList[i].shelves[index]
                                                                                         .items[item_index].value))
