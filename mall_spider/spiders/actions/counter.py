# coding: utf-8

class Counter(object):
    def __init__(self):
        super(Counter, self).__init__()
        self.count = 0

    def increment_and_get(self):
        self.count = self.count + 1
        return self.count

    def get(self):
        return self.count
