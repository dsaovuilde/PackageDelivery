
class HashTable:
    # constructor with default size 40 due to number of packages.
    def __init__(self, size=40):
        self.save_key = None
        self.save_value = None
        self.input_counter = 0
        self.table = []
        for i in range(size):
            self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        if len(self.table[bucket]) != 0:
            self.save_key = key
            self.save_value = value
            self.double(len(self.table), self.table)
        else:
            self.table[bucket].append(key)
            self.table[bucket].append(value)
            if key == 41:
                print(f'adding Key: {key}, Value: {value} to hash table')

    def lookup(self, item):
        if (len(self.table) in range(40, 50)) & (item not in range(len(self.table))):
            lst = []
            for i in range(len(self.table)):
                if (item == self.table[i][1].get_address()) | (item == self.table[i][1].get_city()) \
                        | (item == self.table[i][1].get_zipcode()) | (item == self.table[i][1].get_deadline())\
                        | (item == self.table[i][1].get_status()) | (item == self.table[i][1].get_notes()):
                    lst.append(self.table[i][1])
            return lst
        else:
            bucket = hash(item) % len(self.table)
        return self.table[bucket][1]

    def double(self, length, table1):
        table2 = HashTable(length * 2)
        for item in table1:
            if len(item) != 0:
                table2.insert(item[0], item[1])

        self.table = table2.table
        self.insert(self.save_key, self.save_value)

    def update(self, index, status):
        bucket = hash(index) % len(self.table)
        self.table[bucket][1].set_status(status)

    def __str__(self):
        return str(self.table)

    def __len__(self):
        return len(self.table)
