import csv
from Graph import Graph, Vertex
from HashTable import HashTable
from Package import Package
from Truck import Truck
from Queue import Queue
from datetime import datetime, timedelta
import click

addresses = []
distances = None
package_table = HashTable()
graph = Graph()
address_table = HashTable(27)
truck1 = Truck('Truck1')
truck2 = Truck('Truck2')
package_list = []
depot = '4001 South 700 E'

with open('WGUPS Package File.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    package_info = [row for row in csv_reader]
    for item in package_info:
        status = 'At Depot'
        s = item[7]
        if s[0:7] == 'Delayed':
            status = 'On Flight'
        package = Package()
        package.set_package_id(int(item[0]))
        package.set_address(item[1])
        package.set_city(item[2])
        package.set_state(item[3])
        package.set_zipcode(item[4])
        package.set_deadline(item[5])
        package.set_weight(int(item[6]))
        package.set_notes(item[7])
        package.set_status(status)
        if status == 'On Flight':
            package.set_delayed()
        if s == 'Can only be on truck 2':
            package.set_requires_specific_truck()
        if s[0:22] == 'Must be delivered with':
            p1 = int(s[23:25])
            p2 = int(s[30:32])
            package.set_accompanying_packages([p1, p2])
        if s == 'Wrong address listed':
            package.set_wrong_address(True)
        package_table.insert(package.get_package_id(), package)
        package_list.append(package)


# distance table was exported into 2 csv files. one for the labels and one for the table.
# this allowed me to use the indexes of the addresses to find the distances.
with open('addresses.csv', encoding='utf-8-sig') as address_file:
    csv_reader = csv.reader(address_file, delimiter=',')
    i = 0
    for row in csv_reader:
        address_table.insert(row[0], i)
        addresses.append(row[0])
        i += 1

# read the distance table into half of an NxN matrix.
with open('WGUPS Distance Table.csv', encoding='utf-8-sig') as distance_table:
    csv_reader = csv.reader(distance_table, delimiter=',')
    distances = [row for row in csv_reader]
    for x in distances:
        try:
            x.remove('')
        except ValueError:
            pass

# Using the address file and distance matrix, addresses are added into a weighted graph.
for address in addresses:
    vertex = Vertex(address)
    graph.add_vertex(address)
    for i in range(addresses.index(address) + 1):
        weight = distances[addresses.index(address)][i]
        if address != addresses[i]:
            graph.add_directed_edge(addresses[i], address, float(weight))
            graph.add_directed_edge(address, addresses[i], float(weight))


def set_route(truck):
    unvisited_queue = Queue()
    curr_address = depot
    list_of_packages = truck.get_packages_on_board()
    for a in graph.adjacency_list[curr_address]:
        for p in list_of_packages:
            if a == p.get_address():
                unvisited_queue.enqueue(a)
                curr_address = p.get_address()
                for x in package_table.lookup(p.get_address()):
                    list_of_packages.remove(x)
    return unvisited_queue


def return_to_depot(truck):
    if truck.get_location() != depot:
        distance_to_return = graph.edge_weights[(truck.get_location(), depot)]
        truck.set_location(depot)
        truck.add_to_mileage(distance_to_return)


def load_truck(truck):
    start = depot
    for address in graph.adjacency_list[start]:
        for package in package_table.lookup(address):
            if package in package_list and not(package.get_delayed()):
                if truck.inventory == truck.capacity or len(package_list) == 0:
                    break
                truck.load(package)
                truck.unvisited_queue.enqueue(address)
                start = address
                package_list.remove(package)


def deliver(cutoff_time=datetime.strptime('17:00', '%H:%M')):
    # Move through unvisited queues which have been created by the sorted adjacency list to ensure trucks always move to the closes address
    # The package with the wrong address is corrected at 10:20.
    # Each truck can only hold 16 and there are a total of 40 packages. Truck1 must return to the depot and load the extra 4 packages.
    truck2.set_delayed()
    truck1.set_departure_time()
    truck2.set_departure_time()
    while (len(truck1.unvisited_queue) > 0) | (len(truck2.unvisited_queue) > 0):
        if truck1.get_time() > datetime.strptime('10:20', '%H:%M') or truck2.get_time() > datetime.strptime('10:20', '%H:%M'):
            if package_table.lookup(9).get_address() != '410 S State St':
                package_table.lookup(9).set_address('410 S State St')
                package_table.lookup(9).set_wrong_address(False)
                package_list.append(package_table.lookup(9))

        next_loc_1 = truck1.unvisited_queue.dequeue()
        time_taken1 = round(((graph.edge_weights[(truck1.get_location(), next_loc_1)]) / 18)*60)
        truck1.add_time(time_taken1)
        truck1.add_to_mileage(graph.edge_weights[(truck1.get_location(), next_loc_1)])
        truck1.set_location(next_loc_1)
        for packages in package_table.lookup(next_loc_1):
            packages.set_status(f'Delivered by truck1 at {truck1.get_time()}')
        next_loc_2 = truck2.unvisited_queue.dequeue()
        if not(next_loc_2 is None):
            time_taken2 = round(((graph.edge_weights[(truck2.get_location(), next_loc_2)]) / 18) * 60)
            truck2.add_time(time_taken2)
            truck2.add_to_mileage(graph.edge_weights[(truck2.get_location(), next_loc_2)])
            truck2.set_location(next_loc_2)
        for packages in package_table.lookup(next_loc_2):
            packages.set_status(f'Delivered by truck2 at {truck2.get_time()}')
        if len(truck1.unvisited_queue) == 0:
            return_to_depot(truck1)
            load_truck(truck1)
    truck1.packages_on_board.clear()
    return_to_depot(truck1)
    truck2.packages_on_board.clear()
    return_to_depot(truck2)


for addy in addresses:
    graph.sort_adjacency_list(addy)


load_truck(truck1)
load_truck(truck2)
deliver()


@click.command()
@click.option('--info', default=None, help='look up item(s) in hash table default = 1st item')
def lookup(info):

    """lookup function for package Hash Table. If searching by ID, it will return a specific package.
    if searching by other package information such as address, it will return a list of all packages destined
    to that address. If no argument is provided, this function will print the entire package table.
    Additionally, if the argument provided is not in the package table it will call the insert
    function and add a new item to the package hash table."""

    if info is None:
        print(package_table)
        print(f'Truck 1 miles: {truck1.get_mileage()}')
        print(f'Truck 2 miles: {truck2.get_mileage()}')
    elif package_table.lookup(info) == []:
        package_table.insert(len(package_table) + 1, info)
    else:
        try:
            print(package_table.lookup(int(info)))
        except ValueError:
            print(package_table.lookup(info))


if __name__ == '__main__':
    lookup()



