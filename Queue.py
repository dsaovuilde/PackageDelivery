class Queue:

    def __init__(self,):
        self.data = []

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def isempty(self):
        return len(self.data) == 0

    def enqueue(self, e):
        if self.isempty() or e != self.data[-1]:
            self.data.append(e)

    def dequeue(self):
        if self.isempty():
            print("Empty Queue")
            return
        return self.data.pop(0)

    def first(self):
        if self.isempty():
            print("Empty Queue")
            return
        return self.data[0]






