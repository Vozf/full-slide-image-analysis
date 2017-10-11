class TileStream:
    def __init__(self, func, size):
        self.iteration = -1
        self.max_iteration = size
        self.func = func
        return

    def next(self):
        self.iteration += 1
        if self.iteration < self.max_iteration:
            return self.func(self.iteration)
