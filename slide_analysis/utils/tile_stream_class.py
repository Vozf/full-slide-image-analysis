class TileStream:
    def __init__(self, splitting_service):
        self.iteration = 0
        self.splitting_service = splitting_service

    def __iter__(self):
        return self

    def __next__(self):
        print(str(self.iteration) + '/' + str(len(self)))
        if self.iteration >= len(self):
            raise StopIteration
        res = self.splitting_service._cut_tile(self.iteration)
        self.iteration += 1
        return res

    def __len__(self):
        return len(self.splitting_service)
