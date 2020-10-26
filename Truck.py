from datetime import datetime, timedelta
from Queue import Queue


class Truck:

    def __init__(self, name):
        self.name = name
        self.capacity = 16
        self.inventory = 0
        self.mileage = 0
        self.location = '4001 South 700 E'
        self.packages_on_board = []
        self.full = False
        self.departure_time = None
        self.delayed = False
        self.priority = False
        self.activity_time = None
        self.unvisited_queue = Queue()

    def load(self, package):
        self.packages_on_board.append(package)
        self.inventory += 1
        package.set_loaded()
        if package.get_delayed():
            self.delayed = True
        package.set_status(f'On {self.name}')
        if self.inventory == self.capacity:
            self.full = True

    def deliver(self, package, time):
        print(f"delivering package: {package.get_package_id()}")
        package.set_status(f'Delivered by {self.name} at {time}')
        package.set_delivery_time(time)
        self.packages_on_board.remove(package)
        self.full = False
        self.inventory = self.inventory - 1
        if package.get_deadline() == '09:00':
            self.priority = False

    def get_packages_on_board(self):
        return self.packages_on_board

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def is_full(self):
        return self.full

    def set_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def add_to_mileage(self, dist):
        self.mileage = self.mileage + dist

    def get_mileage(self):
        return self.mileage

    def get_capacity(self):
        return self.capacity

    def get_inventory(self):
        return self.inventory

    def set_departure_time(self):
        if self.delayed:
            self.departure_time = datetime.strptime('09:05', '%I:%M')
        else:
            self.departure_time = datetime.strptime('08:00', '%I:%M')

    def get_departure_time(self):
        return self.departure_time

    def add_time(self, increase_time):
        if self.activity_time is None:
            self.activity_time = self.departure_time
        self.activity_time = self.activity_time + timedelta(minutes=increase_time)

    def get_time(self):
        if self.activity_time is None:
            return self.departure_time
        else:
            return self.activity_time

    def set_delayed(self):
        self.delayed = True

    def __str__(self):
        return str(self.name)
