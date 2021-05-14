
class Edge(object):

    def __init__(self, c, f, t):
        self.max_capacity = int(c)
        self.from_r = f
        self.to_r = t
        self.used_capacity = 0

    def __str__(self):
        return "{} - {} : {}".format(self.max_capacity, self.from_r, self.to_r)

    def add_used_capacity(self, capacity):
        self.used_capacity += capacity

    def get_capacity_difference(self):
        return self.max_capacity - self.used_capacity

    def is_full(self):
        return self.max_capacity == self.used_capacity
