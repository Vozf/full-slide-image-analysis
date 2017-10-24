class TestDescriptor:
    def __init__(self, fictive_param, tile):
        self.tile = tile

    def calc(self):
        (r, g, b, a) = self.tile.data[0]
        self.value = r + g + b
