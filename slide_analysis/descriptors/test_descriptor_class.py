class TestDescriptor:
    def __init__(self, fictive_param):
        pass

    def calc_by_tile(self, tile):
        self.tile = tile
        (r, g, b, a) = self.tile.data[0]
        self.value = r + g + b
        del self.tile.data
