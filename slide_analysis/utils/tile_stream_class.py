class TileStream:
    def __init__(self, func, length):
        self.iteration = 0
        self.length = length
        self.iter_func = func
        return

    def next(self):
        res = self.iter_func(self.iteration)
        self.iteration += 1
        return res

    def has_next(self):
        return self.iteration < self.length

    def for_each(self, func):
        while self.has_next():
            print(str(self.iteration) + '/' + str(self.length))
            func(self.next())
