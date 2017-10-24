class TestDescriptor:
    def __init__(self, fictive_param):
        pass

    def calc(self, tile):
        (r, g, b, a) = tile.data[0]
        value = r + g + b
        return value
