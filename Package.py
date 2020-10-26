class Package:

    def __init__(self):
        self.package_id = None
        self.address = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.deadline = None
        self.weight = None
        self.notes = None
        self.status = None
        self.time_delivered = None
        self.delayed = False
        self.accompanying_packages = None
        self.requires_specific_truck = False
        self.loaded = False
        self.wrong_address = False
        self.delivery_time = None

    def get_package_id(self):
        return self.package_id

    def get_address(self):
        return self.address

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zipcode(self):
        return self.zipcode

    def get_deadline(self):
        return self.deadline

    def get_weight(self):
        return self.weight

    def get_notes(self):
        return self.notes

    def get_status(self):
        return self.status

    def get_delayed(self):
        return self.delayed

    def get_accompanying_packages(self):
        return self.accompanying_packages

    def get_requires_specific_truck(self):
        return self.requires_specific_truck

    def get_loaded(self):
        return self.loaded

    def get_wrong_address(self):
        return self.wrong_address

    def get_delivery_time(self):
        return self.delivery_time

    def set_package_id(self, package_id):
        self.package_id = package_id

    def set_address(self, address):
        self.address = address

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_zipcode(self, zipcode):
        self.zipcode = zipcode

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_weight(self, weight):
        self.weight = weight

    def set_notes(self, notes):
        self.notes = notes

    def set_status(self, status):
        self.status = status

    def set_delayed(self):
        self.delayed = True

    def set_accompanying_packages(self, accompanying_packages):
        self.accompanying_packages = accompanying_packages

    def set_requires_specific_truck(self):
        self.requires_specific_truck = True

    def set_loaded(self):
        self.loaded = True

    def set_wrong_address(self, wrong_address):
        self.wrong_address = wrong_address

    def set_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time

    def update_status(self, status):
        self.status = status

    def __str__(self):
        return f'ID: {self.package_id}, address: {self.address}, {self.city}, {self.state} {self.zipcode}' \
               f' Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes}, Status: {self.status}'

    def __repr__(self):
        return f'{self.package_id}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline}, ' \
               f'{self.weight}, {self.notes}, {self.status}'
