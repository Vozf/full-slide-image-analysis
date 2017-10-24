class TileStream:
    def __init__(self, splitting_service):
        self.iteration = 0
        self.splitting_service = splitting_service

    def next(self):
        res = self.splitting_service._cut_tile(self.iteration)
        self.iteration += 1
        return res

    def has_next(self):
        return self.iteration < len(self)

    def __len__(self):
        return len(self.splitting_service)

    def for_each(self, func):
        while self.has_next():
            print(str(self.iteration) + '/' + str(len(self)))
            func(self.next())
